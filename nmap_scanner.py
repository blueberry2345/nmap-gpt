import nmap
from gpt import get_vulnerability, api_key_valid

# Function that executes a nmap scan and returns the results as a list of dictionaries
def run_nmap(target_ip):
    # port result list
    port_results = []
    # creation of port scanner object
    scanner = nmap.PortScanner()
    # execute nmap scan
    scanner.scan(target_ip, arguments="-T4 -p- -A")

    try:
        # for each protocol in scan results
        for protocol in scanner[target_ip].all_protocols():
            # get list of ports associated with protocol
            ports_list = scanner[target_ip][protocol].keys()

            # for port in list of ports
            for port in ports_list:

                # get port info and add that information in port_results as dictionary
                port_info = scanner[target_ip][protocol][port]

                print(port_info)
                print(type(port_info))
                print(port_info.get('name', 'unknown'))
                try:

                    port_results.append({
                        "Port": port,
                        "State": port_info["state"],
                        "Product": port_info["product"],
                        "Version": port_info["version"],
                        "Full": str(port_info),
                        "Exploits":  get_vulnerability(port_info) if api_key_valid() else []
                    }

                    )

                # Exception if error occurs when gathering results for a port
                except Exception:
                    print("adding port error")
                    pass

    # exception if IP input is invalid
    except KeyError:
        return "Error: invalid IP"



    # Return port results
    return port_results
