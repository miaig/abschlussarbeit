{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
  name = "pipzone";
  targetPkgs = pkgs: (with pkgs; [
    python313
    python313Packages.pip
    python313Packages.virtualenv
  ]);
  runScript = "bash --init-file /etc/profile";
}).env
