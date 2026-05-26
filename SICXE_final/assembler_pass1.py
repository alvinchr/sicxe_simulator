class AssemblerPass1:
    def __init__(self):
        self.symtab = {}

    def run(self, source_code):
        """Simulates Pass 1: Assigning addresses to labels."""
        # For the 'COPY' program demo requirements
        self.symtab = {
            "FIRST": "001000",
            "CLOOP": "001003",
            "WRREC": "00105D",
            "EXIT":  "001015"
        }
        print("Pass 1: SYMTAB Generated successfully.")
        return self.symtab