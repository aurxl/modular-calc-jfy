{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      pandoc
      poetry
      python312
      qtcreator
    ];

  shellHook = ''
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
    poetry env use $(which python)
    source $(poetry env info --path)/bin/activate
  '';

}
