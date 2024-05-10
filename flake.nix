{
inputs.nixpkgs.url = "github:nixos/nixpkgs";
outputs = { self, nixpkgs}:
  let pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in
  {
    devShell.x86_64-linux =
      pkgs.mkShell {
        buildInputs = [
		      pkgs.tk
	      ];

        FONTCONFIG_FILE = pkgs.makeFontsConf { fontDirectories = [
            "/Library/Fonts"
            "/System/Library/Fonts"
            "/Users/USER/Library/Fonts"
        ]; };

        packages = [
          (pkgs.python311Full.withPackages (python-pkgs: [
	  	          python-pkgs.tkinter
		            python-pkgs.argon2-cffi
              ]
            )
          )
        ];
    };
  };
}

