import argparse
import re
import sys
from typing import Any, Dict, List

from module import create_module, remove_module
from utils import parse_cli_fields


def main():
    parser = argparse.ArgumentParser(description="CLI para gerenciamento de módulos Django")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando create
    create_parser = subparsers.add_parser("create", help="Criar um módulo")
    create_parser.add_argument("version", type=str, help="Versão do módulo (ex: v1)")
    create_parser.add_argument("module_name", type=str, help="Nome do módulo (ex: places)")
    create_parser.add_argument(
        "-f", "--fields", type=str,
        help=(
            "Campos do modelo no formato nome=Tipo[:param=valor,...], separados por ponto e vírgula. "
            "Exemplo: name=CharField:max_length=255;active=BooleanField;score=IntegerField"
        )
    )

    # Comando remove
    remove_parser = subparsers.add_parser("remove", help="Remover um módulo")
    remove_parser.add_argument("version", type=str, help="Versão do módulo (ex: v1)")
    remove_parser.add_argument("module_name", type=str, help="Nome do módulo (ex: places)")

    args = parser.parse_args()

    base_dir = "src"

    if args.command == "create":
        processed_fields = parse_cli_fields(args.fields)
        create_module(base_dir, "django_app", args.version, args.module_name, processed_fields)
    elif args.command == "remove":
        remove_module(base_dir, "django_app", args.version, args.module_name)
    else:
        print("Comando não reconhecido")
        sys.exit(1)


if __name__ == "__main__":
    main()