with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sillypaste";
  buildInputs = [
    python3
    poetry
    pre-commit
    postgresql
  ];
  # shellHook = ''
  #   if [[ ! -d venv ]]; then
  #     virtualenv venv
  #   fi
  #   . venv/bin/activate
  # '';
}
