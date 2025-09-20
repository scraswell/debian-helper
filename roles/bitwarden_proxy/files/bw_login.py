import hashlib
import base64

def make_prelogin_key(password: str, email: str, iterations: int = 600000, dklen: int = 32) -> bytes:
    """Step 1: Generate the Prelogin Key using PBKDF2-HMAC-SHA256"""
    password_bytes = password.encode('utf-8')
    salt_bytes = email.encode('utf-8')

    derived_key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt_bytes, iterations, dklen)
    return derived_key  # Returns raw bytes, NOT Base64 yet

def hash_master_key(password: str, master_key: bytes, hash_purpose: str = "server") -> str:
    """Step 2: Hash the Master Key for authentication"""
    password_bytes = password.encode('utf-8')

    # Use `1` iteration for server auth, `2` for local authorization
    iterations = 2 if hash_purpose == "local" else 1

    # PBKDF2-HMAC-SHA256 with `iterations`
    derived_hash = hashlib.pbkdf2_hmac('sha256', master_key, password_bytes, iterations, 32)

    # Convert to Base64 (Bitwarden sends this in `serverMasterKeyHash`)
    return base64.b64encode(derived_hash).decode()

# Example Usage
password = "thisisapassword"
email = "scraswell+bwtest@gmail.com"

# Step 1: Generate Prelogin Key
master_key = make_prelogin_key(password, email)
print("Prelogin Key (Base64):", base64.b64encode(master_key).decode())

# Step 2: Generate Final Hashed Key (Server Authentication)
server_master_key_hash = hash_master_key(password, master_key, hash_purpose="server")
print("Server Master Key Hash (Base64):", server_master_key_hash)

# Step 3: Generate Local Authorization Key (if needed)
local_master_key_hash = hash_master_key(password, master_key, hash_purpose="local")
print("Local Master Key Hash (Base64):", local_master_key_hash)


# curl -kfsSL \
#      -X POST "https://bitwarden.at.home/identity/connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -H "Accept: application/json" \
#      -d "grant_type=password" \
#      -d "client_id=cli" \
#      -d "username=scraswell%2Bbwtest@gmail.com" \
#      -d "password=IMZNhTVF33y9jqOS66P%2BsikLNCPndi8xgc4BgAyD5hs%3D" \
#      -d "scope=api offline_access" \
#      -d "device_identifier=00000000-0000-0000-0000-000000000000" \
#      -d "device_name=Linux CLI" \
#      -d "device_type=25" | jq
# 
# curl -kfsSL \
#      -X POST "https://bitwarden.at.home/identity/connect/token" \
#      -H "Content-Type: application/x-www-form-urlencoded" \
#      -H "Accept: application/json" \
#      -d 'grant_type=refresh_token' \
#      -d 'client_id=undefined' \
#      -d 'refresh_token=Ez7fcqbyJAE68JSKWKFLzSSGZTALLTgiRCNrFMQQCtJPkXR0PXIl4dSBIofX8MtlpGer6TJA2NdHrA5ztFZQwg==' | jq
# 
# curl -kfsSL \
#      -X GET 'https://bitwarden.at.home/api/sync?excludeDomains=true' \
#      -H "Content-Type: application/json" \
#      -H "Accept: application/json" \
#      -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYmYiOjE3NDI0ODQwNjMsImV4cCI6MTc0MjQ5MTI2MywiaXNzIjoiaHR0cDovL2xvY2FsaG9zdHxsb2dpbiIsInN1YiI6ImNlOWI1NmEzLTVmN2ItNGVkMy05MjQzLTk4NmExYmE3NTA5NSIsInByZW1pdW0iOnRydWUsIm5hbWUiOiJTZWFuICh0ZXN0KSIsImVtYWlsIjoic2NyYXN3ZWxsK2J3dGVzdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwic3N0YW1wIjoiYmZhYzA4YTMtZTc2Mi00ZDBiLTlhYWItODM1ZjYyMDYwNTJlIiwiZGV2aWNlIjoiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwic2NvcGUiOlsiYXBpIiwib2ZmbGluZV9hY2Nlc3MiXSwiYW1yIjpbIkFwcGxpY2F0aW9uIl19.nYh5VkSftjiRtIdVSBR8MADNeBAsJ1yEI08wYttoTKPdWoJnJb6wybm4dury4-qGB-cR_vrJjdxrZngzu9a4qW4-G1KMwNLKEl3CCtl4CODLSmUPF00AuNiME6ueoGaXQ9iAR041eYKX_1qxw4YyHvqC0CP1EWfQb_OPaHk0yrqLhJFEfAFZSq5K4oseOnyQGvJQ8FC-dW3yPCq7z6CyZckZx_p0Sxi3jrJezMDMXdh6kbWRGITlyD-32BVjjzUzlOxFqKkXeU79_H1g3KGjwIzwncrbqxhQCKnjHj-Pn0la26nG_ZZQ8lSIDrwvdebylktCk_4bxJH0rl-roqkEGA" \
#      | jq