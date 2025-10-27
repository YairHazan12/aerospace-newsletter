#!/usr/bin/env python3
"""
Newsletter Subscriber Management CLI
Command-line tool for managing newsletter subscribers
"""

import sys
import argparse
from email_manager import EmailManager
import json

def main():
    parser = argparse.ArgumentParser(description='Manage newsletter subscribers')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Subscribe command
    subscribe_parser = subparsers.add_parser('subscribe', help='Subscribe an email')
    subscribe_parser.add_argument('email', help='Email address to subscribe')
    subscribe_parser.add_argument('--name', help='Name of the subscriber')
    
    # Unsubscribe command
    unsubscribe_parser = subparsers.add_parser('unsubscribe', help='Unsubscribe an email')
    unsubscribe_parser.add_argument('email', help='Email address to unsubscribe')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List subscribers')
    list_parser.add_argument('--active-only', action='store_true', help='Show only active subscribers')
    list_parser.add_argument('--format', choices=['table', 'json', 'csv'], default='table', help='Output format')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show subscription statistics')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import subscribers from file')
    import_parser.add_argument('file', help='JSON file with subscribers')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export subscribers to file')
    export_parser.add_argument('--file', help='Output file (default: subscribers_export.json)')
    export_parser.add_argument('--active-only', action='store_true', help='Export only active subscribers')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize email manager
    manager = EmailManager()
    
    if args.command == 'subscribe':
        result = manager.subscribe(args.email, args.name)
        if result['success']:
            print(f"✅ Successfully subscribed {args.email}")
        else:
            print(f"❌ Failed to subscribe {args.email}: {result['message']}")
            sys.exit(1)
    
    elif args.command == 'unsubscribe':
        result = manager.unsubscribe(args.email)
        if result['success']:
            print(f"✅ Successfully unsubscribed {args.email}")
        else:
            print(f"❌ Failed to unsubscribe {args.email}: {result['message']}")
            sys.exit(1)
    
    elif args.command == 'list':
        if args.active_only:
            subscribers = manager.get_active_subscribers()
        else:
            subscribers = manager.get_all_subscribers()
        
        if args.format == 'json':
            print(json.dumps(subscribers, indent=2))
        elif args.format == 'csv':
            if subscribers:
                headers = ['email', 'name', 'active', 'subscribed_at', 'unsubscribed_at']
                print(','.join(headers))
                for sub in subscribers:
                    row = [str(sub.get(h, '')) for h in headers]
                    print(','.join(f'"{r}"' for r in row))
        else:  # table format
            if not subscribers:
                print("No subscribers found")
                return
            
            print(f"{'Email':<30} {'Name':<20} {'Status':<10} {'Subscribed':<12}")
            print("-" * 80)
            for sub in subscribers:
                status = "Active" if sub.get('active', False) else "Inactive"
                name = sub.get('name', 'N/A')[:19]
                subscribed = sub.get('subscribed_at', 'N/A')[:10] if sub.get('subscribed_at') else 'N/A'
                print(f"{sub['email']:<30} {name:<20} {status:<10} {subscribed:<12}")
    
    elif args.command == 'stats':
        stats = manager.get_stats()
        print("📊 Newsletter Statistics")
        print("=" * 30)
        print(f"Active subscribers: {stats['active_subscribers']}")
        print(f"Total subscribers: {stats['total_subscribers']}")
        print(f"Inactive subscribers: {stats['inactive_subscribers']}")
        print(f"Last updated: {stats['last_updated']}")
    
    elif args.command == 'import':
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)
                subscribers = data.get('subscribers', data) if isinstance(data, dict) else data
            
            imported = 0
            failed = 0
            
            for sub in subscribers:
                email = sub.get('email', '')
                name = sub.get('name', '')
                result = manager.subscribe(email, name)
                if result['success']:
                    imported += 1
                else:
                    failed += 1
                    print(f"❌ Failed to import {email}: {result['message']}")
            
            print(f"✅ Imported {imported} subscribers, {failed} failed")
            
        except Exception as e:
            print(f"❌ Error importing subscribers: {e}")
            sys.exit(1)
    
    elif args.command == 'export':
        filename = args.file or 'subscribers_export.json'
        subscribers = manager.export_subscribers(not args.active_only)
        
        try:
            with open(filename, 'w') as f:
                json.dump(subscribers, f, indent=2)
            print(f"✅ Exported {len(subscribers)} subscribers to {filename}")
        except Exception as e:
            print(f"❌ Error exporting subscribers: {e}")
            sys.exit(1)

if __name__ == '__main__':
    main()
