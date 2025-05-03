def mask_email(email: str) -> str:
    try:
        local, domain = email.strip().split('@')
        domain_name, *domain_ext = domain.split('.')

        # --- Mask local part ---
        if len(local) <= 4:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        else:
            masked_local = local[:2] + '*' * (len(local) - 4) + local[-2:]

        # --- Mask domain name ---
        if len(domain_name) <= 2:
            masked_domain_name = domain_name[0] + '*'
        else:
            masked_domain_name = domain_name[0] + '*' * (len(domain_name) - 2) + domain_name[-1]

        # --- Reconstruct full domain ---
        masked_domain = masked_domain_name + '.' + '.'.join(domain_ext)

        return f"{masked_local}@{masked_domain}"
    except Exception as e:
        return f"Invalid email format: {str(e)}"