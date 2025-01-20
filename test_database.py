from sqlalchemy import text
from src.database import get_db


def analyze_flight_data():
    try:
        db = next(get_db())

        query = text("""
            SELECT 
                f.flight_number,
                f.departure_datetime,
                ps.outbound_price,
                ps.return_price,
                ps.timestamp as price_snapshot_time,
                so.timestamp as search_time
            FROM search_operations so
            JOIN price_snapshots ps ON ps.search_id = so.id
            JOIN flights f ON ps.flight_id = f.id
            ORDER BY so.timestamp DESC, f.departure_datetime
            LIMIT 10;
        """)

        result = db.execute(query)

        print("\nRecent Flight Prices:")
        print("Flight | Departure Time | Outbound € | Return € | Recorded At")
        print("-" * 80)

        for row in result:
            print(f"{row.flight_number} | "
                  f"{row.departure_datetime} | "
                  f"€{row.outbound_price:.2f} | "
                  f"€{row.return_price:.2f} | "
                  f"{row.price_snapshot_time}")

        # Also show a summary
        summary_query = text("""
            SELECT 
                COUNT(DISTINCT so.id) as search_count,
                COUNT(DISTINCT f.flight_number) as tracked_flights,
                COUNT(ps.id) as total_price_records
            FROM search_operations so
            LEFT JOIN price_snapshots ps ON ps.search_id = so.id
            LEFT JOIN flights f ON ps.flight_id = f.id
        """)

        summary = db.execute(summary_query).fetchone()
        print("\nDatabase Summary:")
        print(f"Total searches conducted: {summary.search_count}")
        print(f"Unique flights tracked: {summary.tracked_flights}")
        print(f"Total price records: {summary.total_price_records}")

        db.close()

    except Exception as e:
        print(f"Error analyzing flight data: {str(e)}")


if __name__ == "__main__":
    analyze_flight_data()