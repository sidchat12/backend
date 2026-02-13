
import asyncio
import os
import sys
import traceback

# Add backend directory to path
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.graph.portfolio_graph import build_portfolio_graph

async def debug_analysis():
    print("Building graph...", flush=True)
    try:
        graph = build_portfolio_graph()
        
        initial_state = {
            "github_url": "https://github.com/abhi-india05",
            "target_role": "Backend Engineer",
            "repo_data": [],
            "profile_data": {}
        }

        print(f"Invoking graph for {initial_state['github_url']}...", flush=True)
        final_state = await graph.ainvoke(initial_state)
        print("Graph execution successful.", flush=True)
        print("Final Report:", flush=True)
        # Handle non-serializable objects in report
        import json
        try:
            print(json.dumps(final_state.get("final_report"), default=str, indent=2), flush=True)
        except Exception:
            print(final_state.get("final_report"), flush=True)

    except Exception as e:
        print(f"Graph execution failed! Error: {e}", flush=True)
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    asyncio.run(debug_analysis())
