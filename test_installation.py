"""
Test script to verify Watchtower installation.
"""

def test_imports():
    """Test that all required modules can be imported."""
    
    print("Testing Watchtower installation...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import duckdb
        print("✅ DuckDB imported successfully")
    except ImportError as e:
        print(f"❌ DuckDB import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    try:
        from pydantic_settings import BaseSettings
        print("✅ Pydantic Settings imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic Settings import failed: {e}")
        return False
    
    # Optional imports
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"⚠️  Streamlit import failed: {e} (optional)")
    
    try:
        import pandas
        print("✅ Pandas imported successfully")
    except ImportError as e:
        print(f"⚠️  Pandas import failed: {e} (optional)")
    
    try:
        import numpy
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"⚠️  NumPy import failed: {e} (optional)")
    
    try:
        import plotly
        print("✅ Plotly imported successfully")
    except ImportError as e:
        print(f"⚠️  Plotly import failed: {e} (optional)")
    
    return True

def test_database():
    """Test database initialization."""
    
    print("\nTesting database initialization...")
    
    try:
        from database import init_database
        conn = init_database()
        print("✅ Database initialized successfully")
        
        # Test a simple query
        result = conn.execute("SELECT COUNT(*) FROM kpis").fetchone()
        print(f"✅ Database query test passed (KPIs table has {result[0]} records)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    
    print("\nTesting configuration...")
    
    try:
        from config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"   Database path: {settings.database_path}")
        print(f"   API port: {settings.api_port}")
        print(f"   Streamlit port: {settings.streamlit_port}")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Run all tests."""
    
    print("🛡️ Watchtower Installation Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    if not imports_ok:
        print("\n❌ Core dependencies missing. Please install requirements:")
        print("   pip install -r requirements-minimal.txt")
        return False
    
    # Test configuration
    config_ok = test_config()
    
    # Test database
    db_ok = test_database()
    
    print("\n" + "=" * 40)
    
    if imports_ok and config_ok and db_ok:
        print("🎉 All tests passed! Watchtower is ready to use.")
        print("\nNext steps:")
        print("   python main.py --mode both")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    main()
