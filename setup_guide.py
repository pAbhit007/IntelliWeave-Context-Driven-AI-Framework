#!/usr/bin/env python3
"""
Quick setup guide and environment checker for the AI Engineer Assignment
"""
import os
import sys
import subprocess
import requests

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment setup...")
    
    issues = []
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        issues.append("❌ .env file not found. Please create it with your API keys.")
    else:
        print("✅ .env file found")
        
        # Check for required environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ['GOOGLE_API_KEY', 'OPENWEATHER_API_KEY']
        for var in required_vars:
            if not os.getenv(var):
                issues.append(f"❌ {var} not set in .env file")
            else:
                print(f"✅ {var} is set")
    
    # Check if Qdrant is running
    try:
        response = requests.get('http://localhost:6333/health')
        if response.status_code == 200:
            print("✅ Qdrant is running")
        else:
            issues.append("❌ Qdrant is not responding properly")
    except requests.RequestException:
        issues.append("❌ Qdrant is not running. Start it with: docker run -d -p 6333:6333 qdrant/qdrant")
    
    # Check if sample PDF exists
    if os.path.exists('data/documents/sample_document.pdf'):
        print("✅ Sample PDF found")
    else:
        issues.append("❌ Sample PDF not found")
    
    # Check virtual environment
    if sys.prefix != sys.base_prefix:
        print("✅ Virtual environment is active")
    else:
        issues.append("❌ Virtual environment not active. Run: source venv/bin/activate")
    
    return issues

def print_setup_instructions():
    """Print setup instructions"""
    print("\n📋 Setup Instructions:")
    print("=" * 50)
    
    print("\n1. Create virtual environment:")
    print("   python3 -m venv venv")
    print("   source venv/bin/activate")
    
    print("\n2. Install dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n3. Start Qdrant:")
    print("   docker run -d -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant")
    
    print("\n4. Create .env file with your API keys:")
    print("   GOOGLE_API_KEY=your_google_api_key")
    print("   OPENWEATHER_API_KEY=your_openweather_api_key")
    print("   LANGCHAIN_API_KEY=your_langchain_api_key")
    
    print("\n5. Run the application:")
    print("   python main.py  # CLI mode")
    print("   streamlit run src/ui/streamlit_app.py  # Web UI")

def main():
    """Main setup guide"""
    print("🚀 AI Engineer Assignment - Setup Guide")
    print("=" * 50)
    
    issues = check_environment()
    
    if not issues:
        print("\n🎉 Environment setup is complete!")
        print("\n💡 You can now run:")
        print("   python main.py")
        print("   streamlit run src/ui/streamlit_app.py")
        
        print("\n📝 Example queries to try:")
        print("   - 'What's the weather in London?'")
        print("   - 'Tell me about artificial intelligence'")
        print("   - 'What are the technology trends?'")
        
    else:
        print(f"\n⚠️  Found {len(issues)} issues:")
        for issue in issues:
            print(f"   {issue}")
        
        print_setup_instructions()
        
        print("\n🔗 Get API keys:")
        print("   Google AI: https://makersuite.google.com/app/apikey")
        print("   OpenWeather: https://openweathermap.org/api")
        print("   LangSmith: https://smith.langchain.com/")

if __name__ == '__main__':
    main()