import sys
from src.ai_engine import AITestEngine
from src.generator import TestFactory

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_file.py>")
        return

    target_file = sys.argv[1]
    
    try:
        engine = AITestEngine()
        factory = TestFactory(engine)
        
        result_path = factory.create_test_file(target_file)
        print(f"✅ Success! Generated: {result_path}")
        
        # Run the tests
        exit_code, error_message = factory.run_tests(result_path)
        
        # Self-healing: if tests failed, attempt to fix the code
        if exit_code != 0:
            print("\n🔧 Attempting to Self-Heal the code...")
            
            # Read the original buggy file
            with open(target_file, "r") as f:
                source_code = f.read()
            
            # Ask AI to fix it
            fixed_code = engine.heal_code(source_code, error_message)
            
            # Overwrite with the fixed code
            with open(target_file, "w") as f:
                f.write(fixed_code)
            
            print(f"✨ Code healed! Re-running tests...\n")
            
            # Run tests again
            factory.run_tests(result_path)
        else:
            print("🎉 Code is already healthy. Work complete!")
        
    except Exception as e:
        print(f"💥 Error: {e}")

if __name__ == "__main__":
    main()
