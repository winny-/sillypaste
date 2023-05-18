with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sillypaste";
  buildInputs = [
    python3
    python3Packages.poetry
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
