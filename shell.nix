{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      poetry
      pandoc
      python312
      python312Packages.pyqt6
      # python312Packages.pytest
      qtcreator
      stdenv.cc.cc.lib
    ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  shellHook = ''
    if [ "$TERM_PROGRAM" != "vscode" ]; then
      poetry env use $(which python)
      source $(poetry env info --path)/bin/activate
    fi
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
  '';

}
