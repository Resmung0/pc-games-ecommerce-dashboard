from pandas import DataFrame, Series
from .utils import ColumnExpander
import altair as alt

def visualize_publisher_column(dataframe: DataFrame) -> Series:
    return dataframe.publisher.value_counts(ascending=False).iloc[:10]

def visualize_developer_column(dataframe: DataFrame) -> Series:
    return dataframe.developer.value_counts(ascending=False).iloc[:10]

def visualize_rate_column(dataframe: DataFrame) -> Series:
    return dataframe.rate.value_counts(ascending=True)

def visualize_price_column(dataframe: DataFrame) -> Series:
    return (
        alt.Chart(dataframe)
        .transform_density('price', as_=['price', 'density'])
        .mark_area()
        .encode(x="price:Q", y='density:Q')
    )

def visualize_drm_column(dataframe: DataFrame) -> Series:
    columns_to_replace = [
        'ArenaNet',
        "GOG.com",
        'Wargaming',
        'Rockstar Games Social Club',
    ]
    return (
        dataframe.drm
                .replace(columns_to_replace, 'Other')
                .fillna('Other')
                .value_counts(normalize=True, ascending=True)
    )

def visualize_os_column(dataframe: DataFrame) -> Series:
    unique_values = ["Windows", "Mac", "Linux"]
    expander = ColumnExpander(unique_values, column="os")
    return expander.expand(dataframe).sum()

def visualize_game_mode_column(
    dataframe: DataFrame, 
    number_values: int = 5
) -> Series:
    unique_values = [
        'Single-player',
        'Shared/Split Screen',
        'PVP',
        'Online Co-op',
        'Online multiplayer',
        'Multiplayer',
        'Local Coop',
        'Cross-Platform Multiplayer',
        'Local Multi-player',
        'Coop'
    ]
    expander = ColumnExpander(unique_values, column="game_mode")
    return expander.expand(dataframe).sum().sort_values()[number_values:]

def visualize_genre_column(dataframe: DataFrame, number_values: int = 5) -> DataFrame:
    unique_values = [
        'Anime',
        'Action',
        'Adventure',
        'Indie',
        'Simulation',
        'Racing',
        'Management',
        'Funny',
        'Card game',
        'Real Time Strategy',
        'Science Fiction', 
        'Software',
        'Early Access',
        'Fantasy',
        'FPS',
        'Shifts',
        'Fight',
        'RPG',
        'Family',
        'Strategy',
        'Casual',
        'Open World', 
        'Medieval', 
        'Space', 
        'Puzzle', 
        'DLC', 
        'Arcade',
        'Fly', 
        'Sports', 
        'Stealth', 
        'Rogue Like',
        'Platform', 
        'Isometric',
        'Board Game', 
        'Ação Social',
        'Primeira Pessoa',
        'MOBA',
        'Massive Multiplayer',
        'MMO',
        'Horror',
        'Hunt', 
        'Shot', 
        'Sandbox', 
        'Battle Royale',
        'Design and Illustration', 
        'HQ', 
        'PixelArt', 
        'Fishing',
        'Hack and Slash', 
        'Cartoon',
        'War',
        'Zombies', 
        'Survival',
        'Subscription', 
        'Single-player',
        'Point-and-Click', 
        'Remote Play', 
        'Metroidvania', 
        'Exploração', 
        'Ninja',
        'Rogue-lite',
        'Shared/Split Screen',
        'Online multiplayer',
        'Multiplayer', 
        'Coop', 
        'Beat’em Up', 
        'Shoot’em Up', 
        'FMV',
        'Virtual Reality', 
        'Music', 
        'Naval', 
        'Thriller', 
        'Tower Defense',
        'Sci-fi',
        'PvP',
        'RPG Maker',
        'Soccer',
        'Tycoon', 
    ]
    expander = ColumnExpander(unique_values, column="genre")
    return expander.expand(dataframe).sum().sort_values()[-number_values:]
