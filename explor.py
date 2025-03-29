import importlib
import os

def list_package_contents(package_name):
    try:
        # Importer dynamiquement le package
        package = importlib.import_module(package_name)
        
        # Afficher les attributs disponibles dans le package
        print(f"\n📦 Contenu de '{package_name}':")
        for item in dir(package):
            print(f"  - {item}")
        
        # Trouver et afficher les fichiers du package
        if hasattr(package, '__path__'):
            print("\n📂 Fichiers du package:")
            for path in package.__path__:
                print(f"  📍 {path}")
                print("  📜", os.listdir(path))
    
    except ModuleNotFoundError:
        print(f"❌ Le package '{package_name}' n'existe pas.")
    except Exception as e:
        print(f"⚠️ Erreur : {e}")

# Demander à l'utilisateur d'entrer le nom du package
if __name__ == "__main__":
    package_name = input("Entrez le nom du package : ")
    list_package_contents(package_name)

