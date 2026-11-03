import sys

# Complete the function 'login_system' below.
#
# The function should return a tuple containing two functions:
# 1. secure_login(username, password)
# 2. get_login_attempts()

def login_system(credentials, login_attempts):
    # Implement the closure here
    def secure_login(username, password):
        # Implementation here
        # Return "Welcome, {username}!" or "Failed login attempt for {username}"
        pass

    def get_login_attempts():
        # Implementation here
        # Return the login_attempts dictionary
        pass

    return secure_login, get_login_attempts

def main():
    input_data = sys.stdin.read().splitlines()
    if not input_data:
        return
    
    try:
        ptr = 0
        num_users = int(input_data[ptr].strip())
        ptr += 1
        
        credentials = {}
        for _ in range(num_users):
            if ptr >= len(input_data): break
            u, p = input_data[ptr].strip().split(',')
            credentials[u] = p
            ptr += 1
            
        attempts_data = {'success': 0, 'failed': 0}
        secure_login, get_login_attempts = login_system(credentials, attempts_data)
        
        if ptr >= len(input_data): return
        num_attempts = int(input_data[ptr].strip())
        ptr += 1
        
        for _ in range(num_attempts):
            if ptr >= len(input_data): break
            u, p = input_data[ptr].strip().split(',')
            print(secure_login(u, p))
            ptr += 1
            
        stats = get_login_attempts()
        print(f"Login Attempts - Successful: {stats['success']} Failed: {stats['failed']}")
    except Exception as e:
        # Traceback will be captured by driver
        raise e

if __name__ == "__main__":
    main()
