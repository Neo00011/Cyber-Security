import subprocess
import argparse
import os

def get_arguments():
    parser = argparse.ArgumentParser(
        description="Advanced Recon and JS Analysis Pipeline",
        usage="%(prog)s -u <url> -l <location> [-H <headers>] [-c <cookies>] [-j]",
    )

    parser.add_argument("-u", "--url", required=True, help="Target URL to scan (e.g., https://target.com)")
    parser.add_argument("-l", "--location", required=True, help="Output file to save clean endpoints (e.g., endpoints.txt)")
    parser.add_argument("-H", "--headers", help="Custom Header values (e.g., 'Authorization: Bearer xyz')")
    parser.add_argument("-c", "--cookies", help="Session Cookie values (e.g., 'session=abc123xyz')")
    parser.add_argument("-j", "--jscript", action="store_true", help="Filter JS files and send them to LinkFinder")

    return parser.parse_args()


def run_katana(url, location, headers, cookies, jscript):
    print(f"\n[+] Executing Katana in background... (Target: {url})")

    command = [
        "katana", 
        "-u", url, 
        "-o", location, 
        "-depth", "2", 
        "-silent",
        "-ef", "css,png,jpg,jpeg,svg,woff,woff2,ico,html,htm,gif", 
        "-pcs"
    ]

    if headers:
        command.extend(["-H", headers])
    if cookies:
        command.extend(["-c", cookies])
    if jscript:  
        command.extend(["-mr", r".*\.js$"])
 
    try:
        subprocess.run(
            command, 
            timeout=180, 
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL 
        )
        print("[+] Katana scan completed successfully!")

    except subprocess.TimeoutExpired:
        print("\n[!] Timeout (3 mins) reached! Katana stopped, proceeding with collected results...")
    except subprocess.CalledProcessError as e:
        print(f"[-] An error occurred while running Katana: {e}")
    except FileNotFoundError:
        print("[-] ERROR: Katana not found! Ensure it is in your system PATH.")


def run_linkfinder(location):
    print("\n[*] Cleaning Katana output and filtering JS files...")
    
    try:
        with open(location, "r", encoding="utf-8") as file:
            unique_links = set(file.read().splitlines())
    except FileNotFoundError:
        print(f"[-] ERROR: Output file '{location}' not found! Katana might have failed.")
        return

    js_links = [link for link in unique_links if link.endswith(".js")]
    
    if not js_links:
        print("[-] No JavaScript files found to analyze. Terminating LinkFinder phase.")
        return

    total = len(js_links)
    print(f"[+] Found {total} unique JS files. Initializing LinkFinder...\n")
    
    all_results = []
    
    # Dinamik dosya isimlendirmesi (Örn: hedef.txt -> hedef_js_secrets.txt)
    base_name, ext = os.path.splitext(location)
    js_output_file = f"{base_name}_js_secrets{ext}"
    
    for i, url in enumerate(js_links, 1):
        display_url = url if len(url) < 60 else url[:57] + "..."
        print(f"\r[*] Progress [{i}/{total}] Analyzing: {display_url}".ljust(100), end="", flush=True)
        
        try:
            result = subprocess.run(
                [
                    "python3", 
                    "linkfinder.py", 
                    "-i", url,
                    "-o", "cli"
                ],
                capture_output=True,
                text=True,
                timeout=45 
            )
            
            if result.stdout:
                all_results.append(f"\n{'='*50}\n[SOURCE]: {url}\n{'='*50}\n{result.stdout}")
                
        except subprocess.TimeoutExpired:
            print(f"\n    [!] Timeout! Skipped: {url}")
        except FileNotFoundError:
            print("\n    [-] ERROR: linkfinder.py not found! Ensure it's in the current directory.")
            break
        except Exception as e:
            print(f"\n    [-] Error occurred: {e}")
            
    print("\n")
    
    if all_results:
        with open(js_output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(all_results))
        print(f"[+] JS Analysis completed! Secrets saved to '{js_output_file}'.")
    else:
        print("[-] LinkFinder finished but could not find any explicit APIs or secrets.")


if __name__ == "__main__":
    args = get_arguments()

    print("[+] Inputs Successfully Received:")
    print(f"    └── Target URL : {args.url}")
    print(f"    └── Output File: {args.location}")
    print(f"    └── Headers    : {args.headers if args.headers else 'None'}")
    print(f"    └── Cookies    : {args.cookies if args.cookies else 'None'}")
    print(f"    └── JS Only    : {'Yes' if args.jscript else 'No'}")
    
    run_katana(args.url, args.location, args.headers, args.cookies, args.jscript)
    run_linkfinder(args.location)
