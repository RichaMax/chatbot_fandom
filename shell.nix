let
  unstableTarball =
    fetchTarball
      https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz;
  pkgs = import <nixpkgs> {}; 
  unstable = import unstableTarball {};

  shell = pkgs.mkShell {
    packages = [
      unstable.docker
      unstable.just
      unstable.uv
      unstable.python313
      unstable.yarn
    ];
    nativeBuildInputs = with pkgs; [ unstable.pkg-config unstable.rustup];
    buildInputs = with pkgs; [ unstable.openssl ];
  };  
in shell
