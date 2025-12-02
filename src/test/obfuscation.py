# pyinstaller --onefile --noconsole --icon=app.ico --add-data "config.json;." main.py

import argparse
import base64
import marshal
import zlib
import sys
from pathlib import Path

LOADER_TEMPLATE = '''
import base64, marshal
{decompress_import}
a={b64!s}
b=base64.b64decode(a)
{maybe_decompress}
c=marshal.loads(b)
exec(c)
'''

def obfuscate_file(input_path: Path, output_path: Path, compress: bool = False):
    src = input_path.read_text(encoding="utf-8")
    code_obj = compile(src, str(input_path), "exec")

    data = marshal.dumps(code_obj)

    if compress:
        data = zlib.compress(data)
    b64 = base64.b64encode(data).decode("ascii")
    loader = LOADER_TEMPLATE.format(
        b64=repr(b64),
        decompress_import="import zlib" if compress else "",
        maybe_decompress="b=zlib.decompress(b)" if compress else ""
    )
    output_path.write_text(loader, encoding="utf-8")
    print(f"Ofuscado gerado: {output_path} (compress={compress})")

def main():
    p = argparse.ArgumentParser(description="Ofusca um arquivo .py usando marshal+base64 (opção zlib).")
    p.add_argument("input", help="Arquivo .py de entrada")
    p.add_argument("-o", "--output", help="Arquivo .py de saída (padrão: ofuscado_<input>)")
    p.add_argument("--compress", action="store_true", help="Aplicar zlib.compress antes do base64 (recomendado)")
    args = p.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        print("Arquivo de entrada não encontrado:", inp, file=sys.stderr)
        sys.exit(2)
    out = Path(args.output) if args.output else inp.with_name(f"ofuscado_{inp.name}")
    obfuscate_file(inp, out, compress=args.compress)

if __name__ == "__main__":
    main()
