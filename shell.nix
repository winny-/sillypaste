with import <nixpkgs> {};

stdenv.mkDerivation {
  name = "sillypaste";
  buildInputs = [
    python310
    pre-commit
    postgresql
  ];
  shellHook = ''
    if [[ ! -d venv ]]; then
      virtualenv venv
    fi
    . venv/bin/activate
  '';
}
