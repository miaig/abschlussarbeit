{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: with ps; [
      matplotlib
      numpy
      flask
    ]))
  ];
  # shellHook = ''
  #   export SHELL=${pkgs.zsh}/bin/zsh
  #   exec ${pkgs.zsh}/bin/zsh
  # '';
}
