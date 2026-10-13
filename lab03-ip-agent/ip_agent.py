import ipaddress
import httpx
import ollama


# ---------- TOOLS (real Python functions the AI can request) ----------

def check_ip_type(ip: str) -> str:
    """Check if an IP address is public, private, loopback, or invalid.

    Args:
        ip: The IP address to check, e.g. 192.168.1.10

    Returns:
        A short description of the IP type
    """
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return f"{ip} is not a valid IP address."
    if addr.is_loopback:
        return f"{ip} is a loopback address (this machine itself)."
    if addr.is_global:
        return f"{ip} is a public internet address."
    return f"{ip} is a private or reserved address (internal network, not reachable from the internet)."


def lookup_ip(ip: str) -> str:
    """Look up the owner (ISP/organization) and location of a public IP address.

    Args:
        ip: The public IP address to look up, e.g. 8.8.8.8

    Returns:
        Organization and location info for the IP
    """
    try:
        r = httpx.get(f"https://ipinfo.io/{ip}/json", timeout=10)
        data = r.json()
    except Exception as e:
        return f"Lookup failed: {e}"
    if data.get("bogon"):
        return f"{ip} is a private/reserved address. No public info exists."
    return (f"IP: {ip} | Org: {data.get('org')} | City: {data.get('city')} | "
            f"Region: {data.get('region')} | Country: {data.get('country')}")


# ALLOWLIST: the ONLY functions the AI is permitted to run
TOOLS = {
    "check_ip_type": check_ip_type,
    "lookup_ip": lookup_ip,
}


# ---------- AGENT ----------

SYSTEM_PROMPT = """You are a SOC analyst assistant with tools for investigating IP addresses.
When the analyst asks about a specific IP, use your tools. Never guess IP details.
For general cybersecurity questions, answer directly without using tools.
Keep answers short: findings, risk level (Low/Medium/High), and next step."""

history = [{"role": "system", "content": SYSTEM_PROMPT}]

print("IP Agent ready. Type 'quit' to exit.\n")

while True:
    question = input("Analyst: ")
    if question == "quit":
        break

    history.append({"role": "user", "content": question})
    response = ollama.chat(model="llama3.2", messages=history, tools=list(TOOLS.values()))

    # AGENT LOOP: keep going as long as the AI wants to use tools
    while response.message.tool_calls:
        history.append(response.message)

        for call in response.message.tool_calls:
            name = call.function.name
            args = call.function.arguments
            print(f"🔧 AI requested: {name}({args})")

            func = TOOLS.get(name)
            if func is None:
                result = f"Tool '{name}' is not allowed."
            else:
                try:
                    result = func(**args)
                except Exception as e:
                    result = f"Tool error: {e}"

            print(f"   ↳ Result: {result}")
            history.append({"role": "tool", "content": str(result), "tool_name": name})

        response = ollama.chat(model="llama3.2", messages=history, tools=list(TOOLS.values()))

    answer = response.message.content
    history.append({"role": "assistant", "content": answer})
    print("\nSOC AI:", answer, "\n")