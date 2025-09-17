import subprocess
import re
from pydantic import BaseModel
from typing import Optional

def get_ufw_status():
    """
    Gets the status of UFW.

    Returns:
        dict: A dictionary containing the UFW status.
    """
    # WARNING: This function executes a system command with `sudo`.
    # Ensure proper security measures are in place for production environments.
    # `capture_output=True` captures stdout and stderr.
    # `text=True` decodes stdout/stderr as text.
    # `check=True` raises CalledProcessError if the command returns a non-zero exit code.
    try:
        result = subprocess.run(['sudo', '/usr/sbin/ufw', 'status'], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        if "Status: active" in output:
            return {"status": "active"}
        elif "Status: inactive" in output:
            return {"status": "inactive"}
        else:
            return {"status": "unknown", "output": output}
    except FileNotFoundError:
        return {"status": "error", "message": "ufw command not found"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

def get_ufw_rules():
    """
    Gets the rules from UFW.

    Returns:
        dict: A dictionary containing the UFW rules.
    """
    # WARNING: This function executes a system command with `sudo`.
    # Ensure proper security measures are in place for production environments.
    # `capture_output=True` captures stdout and stderr.
    # `text=True` decodes stdout/stderr as text.
    # `check=True` raises CalledProcessError if the command returns a non-zero exit code.
    try:
        result = subprocess.run(['sudo', '/usr/sbin/ufw', 'status'], capture_output=True, text=True, check=True)
        output = result.stdout
        
        parsed_data = {
            "status": "unknown",
            "rules": []
        }

        lines = output.strip().split('\n')

        # Parse UFW status (active/inactive) from the first line of the output.
        status_match = re.match(r"Status: (active|inactive)", lines[0])
        if status_match:
            parsed_data["status"] = status_match.group(1)
        else:
            # If status cannot be parsed, return the default parsed_data.
            return parsed_data

        if parsed_data["status"] == "inactive":
            # If UFW is inactive, there are no rules to parse.
            return parsed_data

        # Find the header and separator lines for rules.
        # The header line contains "To", "Action", "From".
        # The separator line consists of hyphens.
        header_line_index = -1
        separator_line_index = -1

        for i, line in enumerate(lines):
            if "To" in line and "Action" in line and "From" in line and header_line_index == -1:
                header_line_index = i
            elif re.match(r"^-+\s+-+\s+-+$", line) and separator_line_index == -1:
                separator_line_index = i

        if header_line_index == -1 or separator_line_index == -1:
            # If header or separator lines are not found, rules cannot be parsed.
            return parsed_data

        # Extract headers by splitting the header line by two or more spaces.
        header_line = lines[header_line_index]
        headers = [h.strip() for h in re.split(r'\s{2,}', header_line) if h.strip()]

        # Parse rules from the lines following the separator.
        for i in range(separator_line_index + 1, len(lines)):
            line = lines[i].strip()
            if not line:
                continue

            # Split each rule line by two or more spaces.
            parts = re.split(r'\s{2,}', line.strip())
            
            rule = {}
            # Handle different formats of UFW rule output.
            if len(parts) >= 3:
                rule[headers[0]] = parts[0] # To
                rule[headers[1]] = parts[1] # Action
                rule[headers[2]] = parts[2] # From
                parsed_data["rules"].append(rule)
            elif len(parts) == 2:
                # Special handling for rules with 'IN' or 'OUT' in the second part.
                if 'IN' in parts[1] or 'OUT' in parts[1]:
                    action_parts = parts[1].split(' ', 1)
                    rule[headers[0]] = parts[0]
                    rule[headers[1]] = action_parts[0]
                    if len(action_parts) > 1:
                        rule[headers[2]] = action_parts[1]
                    else:
                        rule[headers[2]] = "" # No 'From' specified
                    parsed_data["rules"].append(rule)
                else:
                    # Assume 'From' is empty if not explicitly present.
                    rule[headers[0]] = parts[0]
                    rule[headers[1]] = parts[1]
                    rule[headers[2]] = "" 
                    parsed_data["rules"].append(rule)
            else:
                pass # Skip lines that don't match expected rule format.
        return parsed_data

    except FileNotFoundError:
        return {"status": "error", "message": "ufw command not found"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr}

class Rule(BaseModel):
    action: str # allow, deny, reject, limit
    port: str
    protocol: Optional[str] = None
    direction: Optional[str] = 'in'
    from_ip: Optional[str] = 'any'

def add_ufw_rule(rule: Rule):
    """
    Adds a new rule to UFW.

    Args:
        rule (Rule): The rule to add.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    # WARNING: This function executes a system command with `sudo`.
    # Ensure proper security measures are in place for production environments.
    # `input='y\n'` is used to automatically confirm any prompts from ufw.
    command = ['sudo', '/usr/sbin/ufw']
    if rule.action not in ['allow', 'deny', 'reject', 'limit']:
        return {"status": "error", "message": "Invalid action"}
    
    command.append(rule.action)

    if rule.direction in ['in', 'out']:
        command.append(rule.direction)

    if rule.from_ip and rule.from_ip.lower() != 'any':
        command.extend(['from', rule.from_ip])

    command.append('to')
    command.append('any')

    if rule.port:
        command.append('port')
        command.append(rule.port)

    if rule.protocol:
        command.append('proto')
        command.append(rule.protocol)

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True, input='y\n')

        return {"status": "success", "message": result.stdout.strip()}
    except FileNotFoundError:
        return {"status": "error", "message": "ufw command not found"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr.strip()}

def delete_ufw_rule(rule_id: int):
    """
    Deletes a UFW rule by its ID.

    Args:
        rule_id (int): The ID of the rule to delete.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    # WARNING: This function executes a system command with `sudo`.
    # Ensure proper security measures are in place for production environments.
    # `input='y\n'` is used to automatically confirm the deletion.
    try:
        result = subprocess.run(['sudo', '/usr/sbin/ufw', 'delete', str(rule_id)], capture_output=True, text=True, check=True, input='y\n')
        return {"status": "success", "message": result.stdout.strip()}
    except FileNotFoundError:
        return {"status": "error", "message": "ufw command not found"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr.strip()}

def enable_ufw():
    """
    Enables UFW.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    # WARNING: This function executes a system command with `sudo`.
    # Ensure proper security measures are in place for production environments.
    # `input='y\n'` is used to automatically confirm the enabling of UFW.
    try:
        result = subprocess.run(['sudo', '/usr/sbin/ufw', 'enable'], capture_output=True, text=True, check=True, input='y\n')

        return {"status": "success", "message": result.stdout.strip()}
    except FileNotFoundError:
        return {"status": "error", "message": "ufw command not found"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr.strip()}

def disable_ufw():
    """
    Disables UFW.

    Returns:
        dict: A dictionary containing the result of the operation.
    """
    # WARNING: This function executes a system command with `sudo`.
    # Ensure proper security measures are in place for production environments.
    try:
        result = subprocess.run(['sudo', '/usr/sbin/ufw', 'disable'], capture_output=True, text=True, check=True)
        return {"status": "success", "message": result.stdout.strip()}
    except FileNotFoundError:
        return {"status": "error", "message": "ufw command not found"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": e.stderr.strip()}