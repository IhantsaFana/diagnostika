"""Script pour exécuter tous les tests"""
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def run_test_file(test_file, description):
    """Exécute un fichier de test"""
    print("\n" + "=" * 70)
    print(f"📋 {description}")
    print("=" * 70)
    
    try:
        # Importer et exécuter le module de test
        module_name = test_file.replace('.py', '')
        module = __import__(f'tests.{module_name}', fromlist=[''])
        
        # Exécuter la fonction main si elle existe
        if hasattr(module, '__main__'):
            exec(open(f'tests/{test_file}').read())
        
        return True
    except Exception as e:
        print(f"\n❌ ERREUR dans {test_file}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Exécute tous les tests dans l'ordre"""
    print("\n" + "🚀" * 35)
    print("SUITE COMPLÈTE DE TESTS - SYSTÈME DE DIAGNOSTIC")
    print("🚀" * 35)
    
    tests = [
        ('test_models.py', 'Tests des Modèles de Données'),
        ('test_validation.py', 'Tests de Validation des Entrées'),
        ('test_chargement_donnees.py', 'Tests de Chargement des Données JSON'),
    ]
    
    resultats = []
    
    # Tests unitaires (sans dépendances lourdes)
    print("\n" + "📦" * 35)
    print("PHASE 1: TESTS UNITAIRES")
    print("📦" * 35)
    
    for test_file, description in tests:
        success = run_test_file(test_file, description)
        resultats.append((description, success))
    
    # Tests d'intégration (nécessitent les bibliothèques)
    print("\n" + "🔗" * 35)
    print("PHASE 2: TESTS D'INTÉGRATION")
    print("🔗" * 35)
    
    print("\n⚠️  Les tests d'intégration nécessitent:")
    print("   - numpy")
    print("   - scikit-learn")
    print("   - sentence-transformers")
    print("\nVoulez-vous exécuter les tests d'intégration ? (o/n)")
    
    reponse = input().strip().lower()
    
    if reponse in ['o', 'oui', 'y', 'yes']:
        success = run_test_file('test_integration.py', 'Tests d\'Intégration Complets')
        resultats.append(('Tests d\'Intégration', success))
    else:
        print("\n⏭️  Tests d'intégration ignorés")
        resultats.append(('Tests d\'Intégration', None))
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    total = len(resultats)
    passes = sum(1 for _, success in resultats if success is True)
    echecs = sum(1 for _, success in resultats if success is False)
    ignores = sum(1 for _, success in resultats if success is None)
    
    for description, success in resultats:
        if success is True:
            print(f"✅ {description}")
        elif success is False:
            print(f"❌ {description}")
        else:
            print(f"⏭️  {description} (ignoré)")
    
    print("\n" + "-" * 70)
    print(f"Total: {total} | Passés: {passes} | Échecs: {echecs} | Ignorés: {ignores}")
    print("-" * 70)
    
    if echecs == 0 and passes > 0:
        print("\n🎉 TOUS LES TESTS EXÉCUTÉS ONT RÉUSSI ! 🎉")
        return 0
    elif echecs > 0:
        print(f"\n⚠️  {echecs} test(s) ont échoué")
        return 1
    else:
        print("\n⚠️  Aucun test exécuté")
        return 2

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
