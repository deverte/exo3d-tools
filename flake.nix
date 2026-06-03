{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-26.05";
  };

  outputs = inputs@{ self, nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };

    defaultPythonPackages = pkgs.python313Packages;

    shellPackages = [
      pkgs.pyright
      defaultPythonPackages.python-lsp-server
      defaultPythonPackages.twine
      defaultPythonPackages.venvShellHook
    ];
    getBuildPackages = pythonPackages: [
      pkgs.just
      pythonPackages.build
      pythonPackages.pytest
      pythonPackages.setuptools
    ];
    getPropagatedPackages = pythonPackages: [
      pythonPackages.matplotlib
      pythonPackages.numpy
      pythonPackages.scipy
      pythonPackages.pandas
      pythonPackages.typer
    ];

    buildExo3dToolsPackage = pythonPackages: pythonPackages.buildPythonPackage {
      name = "exo3d-tools";
      format = "pyproject";
      version = "0.2.2"; # managed by justfile
      src = ./.;
      nativeBuildInputs = getBuildPackages pythonPackages;
      buildInputs = getBuildPackages pythonPackages;
      propagatedBuildInputs = getPropagatedPackages pythonPackages;
      meta = {
        homepage = "https://github.com/deverte/exo3d-tools";
        licencse = pkgs.lib.licenses.gpl3;
        platforms = pkgs.lib.platforms.linux ++ pkgs.lib.platforms.darwin;
        maintainers = [ pkgs.lib.maintainers.deverte ];
      };
    };
  in {
    devShells.${system}.default = pkgs.mkShell {
      venvDir = ".venv";
      nativeBuildInputs = shellPackages;
      buildInputs =
        (getBuildPackages defaultPythonPackages) ++
        (getPropagatedPackages defaultPythonPackages);
    };

    packages.${system} = {
      default = buildExo3dToolsPackage defaultPythonPackages;
      "python311" = buildExo3dToolsPackage pkgs.python311Packages;
      "python312" = buildExo3dToolsPackage pkgs.python312Packages;
      "python313" = buildExo3dToolsPackage pkgs.python313Packages;
      "python314" = buildExo3dToolsPackage pkgs.python314Packages;
    };
  };
}
