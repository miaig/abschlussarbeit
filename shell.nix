{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    (pkgs.python3.withPackages (ps: with ps; [
      matplotlib
      numpy
      flask
      rpi-gpio
    ]))
  ];
}
