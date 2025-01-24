import os
import subprocess
import sys
import requests
import random
from colorama import Fore, Style, init

# Initialize colorama for pretty console output
init(autoreset=True)

# ASCII banner
def print_banner():
    print(Fore.RED + Style.BRIGHT + r"""
███████╗███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝
  ███╔╝ █████╗  ██║   ██║███████╗
 ███╔╝  ██╔══╝  ██║   ██║╚════██║
███████╗███████╗╚██████╔╝███████║
╚══════╝╚══════╝ ╚═════╝ ╚══════ 
      By GhostScan
    HACKING BEYOND LIMITS
    """)


# Install required tools and libraries
def install_dependencies():
    print(Fore.CYAN + "[*] Checking and installing dependencies...")

    # Install amass
    if not shutil.which("amass"):
        print(Fore.YELLOW + "[!] Amass not found. Installing Amass...")
        try:
            subprocess.run(["sudo", "apt", "install", "amass", "-y"], check=True)
            print(Fore.GREEN + "[+] Amass installed successfully.")
        except Exception as e:
            print(Fore.RED + f"[!] Amass installation failed: {e}")

    # Install assetfinder
    if not shutil.which("assetfinder"):
        print(Fore.YELLOW + "[!] Assetfinder not found. Installing Assetfinder...")
        try:
            subprocess.run(["go", "install", "github.com/tomnomnom/assetfinder@latest"], check=True)
            go_bin = os.path.expanduser("~/go/bin")
            os.environ["PATH"] += os.pathsep + go_bin
            print(Fore.GREEN + "[+] Assetfinder installed successfully.")
        except Exception as e:
            print(Fore.RED + f"[!] Assetfinder installation failed: {e}")

    # Install massdns
    if not shutil.which("massdns"):
        print(Fore.YELLOW + "[!] MassDNS not found. Installing MassDNS...")
        try:
            subprocess.run(["git", "clone", "https://github.com/blechschmidt/massdns.git"], check=True)
            os.chdir("massdns")
            subprocess.run(["make"], check=True)
            subprocess.run(["sudo", "cp", "bin/massdns", "/usr/local/bin/"], check=True)
            os.chdir("..")
            print(Fore.GREEN + "[+] MassDNS installed successfully.")
        except Exception as e:
            print(Fore.RED + f"[!] MassDNS installation failed: {e}")

    # Install Python dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "colorama"], check=True)
        print(Fore.GREEN + "[+] Python libraries installed successfully.")
    except Exception as e:
        print(Fore.RED + f"[!] Python library installation failed: {e}")

    # Download resolvers for massdns
    resolver_file = "resolvers.txt"
    if not os.path.exists(resolver_file):
        print(Fore.CYAN + "[*] Downloading resolver file...")
        try:
            subprocess.run(
                ["wget", "https://raw.githubusercontent.com/janmasarik/resolvers/master/resolvers.txt", "-O", resolver_file],
                check=True,
            )
            print(Fore.GREEN + "[+] Resolver file downloaded successfully.")
        except Exception as e:
            print(Fore.RED + f"[!] Failed to download resolvers: {e}")


# Enumerate subdomains using Amass and Assetfinder
def enumerate_subdomains(domain):
    print(Fore.CYAN + "[*] Enumerating subdomains...")
    result_file = f"{domain}_subdomains.txt"

    # Step 1: Amass
    if shutil.which("amass"):
        try:
            print(Fore.CYAN + "[*] Running Amass enumeration...")
            subprocess.run(
                ["amass", "enum", "-d", domain, "-o", result_file],
                check=True,
            )
            print(Fore.GREEN + f"[+] Amass results saved in {result_file}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"[!] Amass error: {e}")

    # Step 2: Assetfinder (Fallback)
    if shutil.which("assetfinder"):
        try:
            print(Fore.CYAN + "[*] Running Assetfinder enumeration...")
            with open(result_file, "a") as f:
                subprocess.run(
                    ["assetfinder", "--subs-only", domain],
                    stdout=f,
                    check=True,
                )
            print(Fore.GREEN + f"[+] Assetfinder results appended to {result_file}")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"[!] Assetfinder error: {e}")

    return result_file


# Resolve subdomains using MassDNS
def resolve_subdomains(input_file, domain):
    print(Fore.CYAN + "[*] Resolving subdomains...")
    output_file = f"{domain}_resolved.txt"

    if not shutil.which("massdns"):
        print(Fore.RED + "[!] MassDNS is not installed. Skipping DNS resolution.")
        return input_file

    # Configure MassDNS
    resolver_file = "resolvers.txt"
    if not os.path.exists(resolver_file):
        print(Fore.YELLOW + f"[!] {resolver_file} not found. Ensure it contains valid DNS resolvers.")
        return input_file

    try:
        subprocess.run(
            [
                "massdns",
                "-r", resolver_file,
                "-o", "S",
                "-t", "A",
                "-w", output_file,
                input_file,
            ],
            check=True,
        )
        print(Fore.GREEN + f"[+] Resolved subdomains saved in {output_file}")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[!] MassDNS error: {e}")
        return input_file

    return output_file


# Check for live subdomains with Python requests
def filter_live_subdomains(input_file):
    print(Fore.CYAN + "[*] Checking for live subdomains...")
    output_file = input_file.replace("_resolved.txt", "_live.txt")

    try:
        with open(input_file, "r") as f:
            subdomains = [line.strip().split()[0] for line in f if line.strip()]
        
        live_subdomains = []
        for subdomain in subdomains:
            try:
                response = requests.get(f"http://{subdomain}", timeout=5)
                if response.status_code < 400:
                    live_subdomains.append(subdomain)
                    print(Fore.GREEN + f"[+] {subdomain} is live.")
            except requests.RequestException:
                print(Fore.YELLOW + f"[-] {subdomain} is not live.")

        with open(output_file, "w") as f:
            f.write("\n".join(live_subdomains))
        print(Fore.GREEN + f"[+] Live subdomains saved in {output_file}")
    except Exception as e:
        print(Fore.RED + f"[!] Error checking live subdomains: {e}")
    return output_file


# Main function
def main():
    print_banner()

    # Step 1: Install dependencies
    install_dependencies()

    # Step 2: Input domain
    domain = input(Fore.CYAN + "[?] Enter the target domain: ").strip()
    if not domain:
        print(Fore.RED + "[!] No domain provided. Exiting.")
        return

    # Step 3: Subdomain enumeration
    subdomains_file = enumerate_subdomains(domain)
    if subdomains_file:
        resolved_file = resolve_subdomains(subdomains_file, domain)
        if resolved_file:
            filter_live_subdomains(resolved_file)


if __name__ == "__main__":
    import shutil
    main()
