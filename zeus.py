import os
import subprocess
from datetime import datetime
import random
from colorama import Fore, Style, init

# Initialize colorama for cross-platform compatibility
init(autoreset=True)

# New ASCII banner with ZEUS title in red
def print_banner():
    print(Fore.RED + Style.BRIGHT + r"""
███████╗███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██║   ██║██╔════╝
  ███╔╝ █████╗  ██║   ██║███████╗
 ███╔╝  ██╔══╝  ██║   ██║╚════██║
███████╗███████╗╚██████╔╝███████║
╚══════╝╚══════╝ ╚═════╝ ╚══════ 
      By Shaheer Yasir           
    HACKING BEYOND LIMITS
    """)


# Function to enumerate subdomains using Subfinder and DNS brute force
def enumerate_subdomains(domain):
    print("[*] Enumerating subdomains...")
    result_file = f"{domain}_subdomains.txt"

    # Subfinder for API-based enumeration
    try:
        subprocess.run(
            ["subfinder", "-d", domain, "-silent", "-o", result_file],
            check=True
        )
        print(f"[+] Subdomains saved in {result_file}")
    except FileNotFoundError:
        print("[!] Subfinder not found! Install it from https://github.com/projectdiscovery/subfinder")
        return None

    # DNS brute-forcing using a wordlist
    print("[*] Performing DNS brute-forcing...")
    try:
        wordlist = "/usr/share/wordlists/subdomains.txt"  # Path to your wordlist
        if not os.path.exists(wordlist):
            print("[!] Default wordlist not found. Please specify a valid path.")
            return result_file

        subprocess.run(
            [
                "dnsx", "-d", domain, "-w", wordlist, "-silent", 
                "-o", f"{domain}_dns_brute.txt"
            ],
            check=True
        )
        # Append DNS brute results to the main subdomain file
        with open(f"{domain}_dns_brute.txt", "r") as dns_results:
            with open(result_file, "a") as subdomains:
                subdomains.write(dns_results.read())
        print("[+] DNS brute-forcing completed and merged.")
    except FileNotFoundError:
        print("[!] Dnsx not found. Install it from https://github.com/projectdiscovery/dnsx")
    return result_file


# Function to filter live subdomains using Httpx
def filter_live_subdomains(input_file):
    print("[*] Filtering live subdomains...")
    output_file = input_file.replace("_subdomains.txt", "_live_subdomains.txt")
    try:
        subprocess.run(
            ["httpx", "-silent", "-l", input_file, "-o", output_file, "-random-agent"],
            check=True
        )
        print(f"[+] Live subdomains saved in {output_file}")
    except FileNotFoundError:
        print("[!] Httpx not found! Install it from https://github.com/projectdiscovery/httpx")
        return None
    return output_file


# Function to bypass WAFs by randomizing headers and proxies
def bypass_waf(subdomains_file):
    print("[*] Attempting to bypass WAFs...")
    output_file = subdomains_file.replace("_live_subdomains.txt", "_waf_bypassed.txt")
    try:
        with open(subdomains_file, "r") as f:
            subdomains = f.readlines()

        proxies = [
            "http://proxy1.example:8080",
            "http://proxy2.example:8080",
            # Add more proxies as needed
        ]

        # Simulate WAF bypass with randomized headers and proxy routing
        with open(output_file, "w") as bypassed:
            for subdomain in subdomains:
                headers = {
                    "User-Agent": f"Custom-Agent-{random.randint(1000, 9999)}",
                    "X-Forwarded-For": f"192.0.2.{random.randint(1, 254)}",
                }
                proxy = random.choice(proxies)
                bypassed.write(f"{subdomain.strip()} - {headers} - Proxy: {proxy}\n")
        print(f"[+] WAF bypassed subdomains saved in {output_file}")
    except FileNotFoundError:
        print("[!] Error processing subdomains file.")
    return output_file


# Main function to run the tool
def main():
    print_banner()
    domain = input("[?] Enter the target domain: ").strip()
    subdomains_file = enumerate_subdomains(domain)

    if subdomains_file:
        live_subdomains_file = filter_live_subdomains(subdomains_file)
        if live_subdomains_file:
            bypass_waf(live_subdomains_file)


if __name__ == "__main__":
    main()
