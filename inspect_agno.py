import pkgutil
import importlib
import inspect

print("="*50)
print("--- Inspecting the 'agno' Library ---")
print("="*50)

try:
    import agno
    # Check for a version attribute
    version = getattr(agno, '__version__', 'version not found')
    print(f"\nSuccessfully imported 'agno' (version: {version})\n")
    
    # Get the path to the installed package
    package_path = agno.__path__

    # Walk the package and list contents
    for _, module_name, _ in pkgutil.walk_packages(path=package_path, prefix=agno.__name__ + '.'):
        print(f"\n--- Contents of module: '{module_name}' ---")
        try:
            module = importlib.import_module(module_name)
            for name in dir(module):
                # Skip private/special attributes
                if not name.startswith('_'):
                    obj = getattr(module, name)
                    # Print classes and functions
                    if inspect.isclass(obj) or inspect.isfunction(obj):
                        obj_type = 'class' if inspect.isclass(obj) else 'function'
                        print(f"  - {name} ({obj_type})")
        except Exception as e:
            print(f"  Could not inspect module {module_name}: {e}")

except ImportError:
    print("\nFATAL ERROR: Could not import the 'agno' library at all.")
    print("Please ensure it is installed correctly in your virtual environment.")

print("\n" + "="*50)
print("--- Inspection Complete ---")
print("="*50)