{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.11";
  };

  outputs = inputs@{ self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
    python = pkgs.python311;
    pythonPackages = pkgs.python311Packages;

    buildPackages = [
      pkgs.just
      python
      pythonPackages.build
      pythonPackages.pytest
      pythonPackages.setuptools
    ];
    shellPackages = [
      pkgs.nodePackages.pyright
      pythonPackages.python-lsp-server
      pythonPackages.twine
      pythonPackages.venvShellHook
    ];
    propagatedPackages = [
      pythonPackages.matplotlib
      pythonPackages.numpy
      pythonPackages.scipy
      pythonPackages.pandas
      pythonPackages.typer
    ];
  in {
    devShells.${system}.default = pkgs.mkShell {
      venvDir = ".venv";
      nativeBuildInputs = shellPackages;
      buildInputs = buildPackages ++ propagatedPackages;
    };

    packages.${system}.default = pythonPackages.buildPythonPackage {
      name = "exo3d-tools";
      format = "pyproject";
      version = "0.2.0"; # managed by justfile
      src = ./.;
      nativeBuildInputs = buildPackages;
      buildInputs = buildPackages;
      propagatedBuildInputs = propagatedPackages;
      meta = {
        homepage = "https://gitea.zarux.ru/astro/exo3d-tools";
        licencse = pkgs.lib.licenses.gpl3;
        platforms = pkgs.lib.platforms.linux ++ pkgs.lib.platforms.darwin;
        maintainers = [ pkgs.lib.maintainers.deverte ];
      };
    };
  };
}
