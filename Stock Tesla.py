import yfinance as yf
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def fetch_stock_data(symbol):
    # Fetch stock data using yfinance
    stock_data = yf.download(symbol, start="2023-01-01", end="2024-01-01")
    return stock_data


def plot_stock_chart(stock_data, chart_frame):
    # Plot stock chart
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(stock_data['Close'], label='Close Price', color='blue')
    ax.set_title('Stock Chart - Tesla (TSLA)', fontsize=14)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD)', fontsize=12)
    ax.grid(True)
    ax.legend()

    # Embed the plot into Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def main():
    # Create Tkinter window
    window = tk.Tk()
    window.title("Stock Market - Tesla (TSLA)")
    window.geometry("800x600")

    # Create a frame for the chart
    chart_frame = ttk.Frame(window)
    chart_frame.pack(fill=tk.BOTH, expand=True)

    # Fetch Tesla (TSLA) stock data
    tsla_data = fetch_stock_data('TSLA')

    # Plot Tesla (TSLA) stock chart
    plot_stock_chart(tsla_data, chart_frame)

    # Run Tkinter event loop
    window.mainloop()


if __name__ == "__main__":
    main()