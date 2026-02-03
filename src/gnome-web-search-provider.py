#!/usr/bin/python3
import subprocess
import html
from dasbus.connection import SessionMessageBus
from dasbus.loop import EventLoop
from dasbus.typing import *

# Configuration
BUS_NAME = "org.gnome.WebSearch.SearchProvider"
OBJECT_PATH = "/org/gnome/WebSearch/SearchProvider"

class GoogleSearchProvider(object):
    # We define the raw XML to ensure strict compatibility with GNOME Shell's interface
    __dbus_xml__ = """
    <node>
        <interface name="org.gnome.Shell.SearchProvider2">
            <method name="GetInitialResultSet">
                <arg direction="in" type="as" name="terms" />
                <arg direction="out" type="as" name="results" />
            </method>
            <method name="GetSubsearchResultSet">
                <arg direction="in" type="as" name="previous_results" />
                <arg direction="in" type="as" name="terms" />
                <arg direction="out" type="as" name="results" />
            </method>
            <method name="GetResultMetas">
                <arg direction="in" type="as" name="results" />
                <arg direction="out" type="aa{sv}" name="metas" />
            </method>
            <method name="ActivateResult">
                <arg direction="in" type="s" name="result" />
                <arg direction="in" type="as" name="terms" />
                <arg direction="in" type="u" name="timestamp" />
            </method>
            <method name="LaunchSearch">
                <arg direction="in" type="as" name="terms" />
                <arg direction="in" type="u" name="timestamp" />
            </method>
        </interface>
    </node>
    """

    def GetInitialResultSet(self, terms: List[str]) -> List[str]:
        # Return the search query itself as the result ID
        return [" ".join(terms)]

    def GetSubsearchResultSet(self, previous_results: List[str], terms: List[str]) -> List[str]:
        return [" ".join(terms)]

    def GetResultMetas(self, results: List[str]) -> List[Dict[str, Variant]]:
        metas = []
        for query in results:
            metas.append({
                "id": Variant("s", query),
                "name": Variant("s", f"Search Google for '{query}'"),
                "description": Variant("s", "Press Enter to open in browser"),
                "icon": Variant("s", "web-browser")
            })
        return metas

    def ActivateResult(self, result: str, terms: List[str], timestamp: int):
        # Open the browser
        url = f"https://www.google.com/search?q={html.escape(result)}"
        subprocess.Popen(["xdg-open", url])

    def LaunchSearch(self, terms: List[str], timestamp: int):
        pass
    
if __name__ == "__main__":
    try:
        from dasbus.loop import EventLoop
        from dasbus.connection import SessionMessageBus
        
        bus = SessionMessageBus()
        
        # Manually register the object with the raw XML interface
        # This is a bit of a hack to ensure GNOME sees exactly what it expects
        provider = GoogleSearchProvider()
        bus.publish_object(OBJECT_PATH, provider)
        
        # Register the name LAST, after the object is ready
        bus.register_service(BUS_NAME)
        
        print(f"Service running at {BUS_NAME}...")
        EventLoop().run()
    except Exception as e:
        print(f"Error starting service: {e}")
        
