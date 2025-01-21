### Zeus Tool - Hacking Beyond Limits
Zeus is a subdomain enumeration and WAF-bypassing tool designed to help ethical hackers and penetration testers discover subdomains of a target and filter live ones while attempting to bypass web application firewalls (WAFs).

### Features
Subdomain Enumeration:
Utilizes Subfinder for API-based enumeration.
Performs DNS brute-forcing using a wordlist.
Live Subdomain Filtering:
Filters live subdomains using Httpx with randomized user agents.
WAF Bypass Simulation:
Adds randomized headers and routes traffic through proxies to simulate WAF bypass.
Stylish Interface:
Includes a red Neue font banner with the tagline "Hacking Beyond Limits".
Output Files:
Saves results into separate files for easier analysis:
<domain>_subdomains.txt
<domain>_live_subdomains.txt
<domain>_waf_bypassed.txt

### Installation
Follow these steps to install and configure Zeus:

1. Clone the Repository
bash
git clone https://github.com/<your-repo>/zeus-tool.git
cd zeus-tool
2. Install Python Dependencies
Install colorama and other required Python libraries:

bash
pip install colorama

3. Install External Tools
Zeus relies on several external tools for subdomain enumeration and filtering. Install them as follows:

Subfinder
sudo apt update
sudo apt install -y subfinder
Or download it from the official repository: https://github.com/projectdiscovery/subfinder.

Dnsx
sudo apt install dnsx
Or download it from the official repository: https://github.com/projectdiscovery/dnsx.

Httpx
sudo apt install httpx
Or download it from the official repository: https://github.com/projectdiscovery/httpx.

4. Wordlist for DNS Brute-forcing
Ensure you have a valid wordlist for DNS brute-forcing. You can use the following example:

bash
sudo apt install wordlists
Or download SecLists:

bash
git clone https://github.com/danielmiessler/SecLists.git
Usage

Run Zeus
Execute Zeus using Python:

python zeus.py
Workflow
Enter the target domain when prompted:

Subdomain enumeration with Subfinder.
DNS brute-forcing using Dnsx.
Live subdomain filtering using Httpx.
WAF bypass simulation by randomizing headers and proxies.
Check the output files:

example.com_subdomains.txt: Raw subdomains.
example.com_live_subdomains.txt: Live subdomains.
example.com_waf_bypassed.txt: WAF bypassed results.
