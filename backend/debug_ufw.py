from ufw_service import get_ufw_rules

if __name__ == "__main__":
    rules = get_ufw_rules()
    print(rules)
