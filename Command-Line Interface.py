import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from scraper import scrape_books, search_book, save_to_file, load_from_file

console = Console()

@click.group()
def cli():
    """📚 Book Scraper CLI — Scrape and interact with online book data."""
    pass

@cli.command()
@click.option('--url', prompt='Enter the URL to scrape from', help='Base URL of the book site')
def scrape(url):
    """🔍 Scrape book data from a given URL."""
    console.print(f"Scraping from: [bold green]{url}[/bold green]")
    books = scrape_books(url)
    if books:
        console.print(f"✅ Scraped [bold cyan]{len(books)}[/bold cyan] books!")
    else:
        console.print("[bold red]❌ No books found![/bold red]")

@cli.command()
@click.argument('query')
def search(query):
    """🔎 Search for a book by title."""
    data = load_from_file()
    results = search_book(data, query)
    if results:
        table = Table(title=f"Search Results for '{query}'")
        table.add_column("Title", style="cyan")
        table.add_column("Price", style="green")
        for book in results:
            table.add_row(book['title'], book['price'])
        console.print(table)
    else:
        console.print(f"[yellow]No results found for[/yellow] [bold]{query}[/bold]")

@cli.command()
@click.option('--filename', default='books.json', help='File to save the data')
def save(filename):
    """💾 Save scraped data to a file."""
    data = scrape_books()
    if data:
        save_to_file(data, filename)
        console.print(f"✅ Data saved to [bold green]{filename}[/bold green]")
    else:
        console.print("[red]❌ No data to save.[/red]")

@cli.command()
@click.option('--filename', default='books.json', help='File to load data from')
def list(filename):
    """📄 List all books from a saved file."""
    data = load_from_file(filename)
    table = Table(title="Saved Books")
    table.add_column("Title", style="cyan")
    table.add_column("Price", style="green")
    for book in data:
        table.add_row(book['title'], book['price'])
    console.print(table)

@cli.command()
def interactive():
    """🧠 Interactive mode to explore books."""
    if not Confirm.ask("Do you want to load previously saved data?"):
        console.print("[red]Aborted.[/red]")
        return

    data = load_from_file()
    while True:
        q = Prompt.ask("Enter a keyword to search (or 'exit' to quit)")
        if q.lower() == 'exit':
            break
        results = search_book(data, q)
        if results:
            for book in results:
                console.print(f"[bold green]{book['title']}[/bold green] - {book['price']}")
        else:
            console.print("[yellow]No matches found.[/yellow]")

if __name__ == "__main__":
    cli()



