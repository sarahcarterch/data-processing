import logging
import os
import sqlite3

import common
import pandas as pd
import pdf_converter


def main():
    # Set path for SQLite database
    db_path = os.path.join("data", "GrosserRat.db")

    # 100307
    csv_mitglieder = os.path.join("data_orig", "100307_gr_mitglieder.csv")
    df_adr = pd.read_csv(csv_mitglieder)
    columns_to_index = [
        "ist_aktuell_grossrat",
        "anrede",
        "titel",
        "gebdatum",
        "gr_wahlkreis",
        "partei",
        "partei_kname",
    ]
    create_sqlite_table(
        db_path, df_adr, "Mitglieder", columns_to_index=columns_to_index
    )

    # 100308
    csv_mitgliedschaften = os.path.join("data_orig", "100308_gr_mitgliedschaften.csv")
    df_mit = pd.read_csv(csv_mitgliedschaften)
    columns_to_index = [
        "kurzname_gre",
        "name_gre",
        "gremientyp",
        "funktion_adr",
        "anrede",
        "name_vorname",
        "partei_kname",
    ]
    create_sqlite_table(
        db_path, df_mit, "Mitgliedschaften", columns_to_index=columns_to_index
    )

    # 100309
    csv_interessensbindungen = os.path.join(
        "data_orig", "100309_gr_interessensbindungen.csv"
    )
    df_int = pd.read_csv(csv_interessensbindungen)
    columns_to_index = ["rubrik", "funktion", "anrede", "name_vorname", "partei_kname"]
    create_sqlite_table(
        db_path, df_int, "Interessensbindungen", columns_to_index=columns_to_index
    )

    # 100310
    csv_gremien = os.path.join("data_orig", "100310_gr_gremien.csv")
    df_gre = pd.read_csv(csv_gremien)
    columns_to_index = ["ist_aktuelles_gremium", "kurzname", "name", "gremientyp"]
    create_sqlite_table(db_path, df_gre, "Gremien", columns_to_index=columns_to_index)

    # 100311
    csv_geschaefte = os.path.join("data_orig", "100311_gr_geschaefte.csv")
    df_ges = pd.read_csv(csv_geschaefte)
    # Create SQLite dataset
    columns_to_index = [
        "status_ges",
        "ga_rr_gr",
        "anrede_urheber",
        "name_vorname_urheber",
        "partei_kname_urheber",
        "anrede_miturheber",
        "name_vorname_miturheber",
        "partei_kname_miturheber",
    ]
    create_sqlite_table(
        db_path, df_ges, "Geschaefte", columns_to_index=columns_to_index
    )

    # 100312
    csv_zuweisungen = os.path.join("data_orig", "100312_gr_zuweisungen.csv")
    df_zuw = pd.read_csv(csv_zuweisungen)
    columns_to_index = [
        "kurzname_an",
        "name_an",
        "status_zuw",
        "status_ges",
        "ga_rr_gr",
        "departement_ges",
        "kurzname_von",
        "name_von",
    ]
    create_sqlite_table(
        db_path, df_zuw, "Zuweisungen", columns_to_index=columns_to_index
    )

    # 100313
    csv_dokumente = os.path.join("data_orig", "100313_gr_dokumente.csv")
    csv_dokumente_md = os.path.join(
        "data_orig", "100313_gr_dokumente_with_markdown.csv"
    )

    # Load with markdown if exists, fallback to base CSV
    if os.path.exists(csv_dokumente_md):
        df_dok = pd.read_csv(csv_dokumente_md)
    else:
        df_dok = pd.read_csv(csv_dokumente)

    for method in ["docling", "pymupdf", "pymupdf4llm"]:
        colname = f"url_dok_md_{method}"
        if colname not in df_dok.columns:
            df_dok[colname] = None
        mask = df_dok[colname].isna() | (df_dok[colname] == "")
        if mask.any():
            df_dok.loc[mask, :] = pdf_converter.add_markdown_column(
                df_dok.loc[mask, :], "url_dok", method, csv_output_path=csv_dokumente_md
            )

    # Save updated DataFrame with markdown
    df_dok.to_csv(csv_dokumente_md, index=False)

    columns_to_index = ["titel_dok", "status_ges", "ga_rr_gr", "departement_ges"]
    create_sqlite_table(db_path, df_dok, "Dokumente", columns_to_index=columns_to_index)

    # 100314
    csv_vorgaenge = os.path.join("data_orig", "100314_gr_vorgaenge.csv")
    df_vor = pd.read_csv(csv_vorgaenge)
    columns_to_index = ["Vermerk", "status_ges", "ga_rr_gr", "departement_ges"]
    create_sqlite_table(db_path, df_vor, "Vorgaenge", columns_to_index=columns_to_index)

    # 100348
    csv_traktanden = os.path.join("data_orig", "100348_gr_traktanden.csv")
    csv_traktanden_md = os.path.join(
        "data_orig", "100348_gr_traktanden_with_markdown.csv"
    )

    # Load with markdown if exists, fallback to base CSV
    if os.path.exists(csv_traktanden_md):
        df_trakt = pd.read_csv(csv_traktanden_md)
    else:
        df_trakt = pd.read_csv(csv_traktanden)

    for pdf_column in ["url_tagesordnung_dok", "url_vollprotokoll"]:
        for method in ["docling", "pymupdf", "pymupdf4llm"]:
            colname = f"{pdf_column}_md_{method}"
            if colname not in df_trakt.columns:
                df_trakt[colname] = None
            mask = df_trakt[colname].isna() | (df_trakt[colname] == "")
            if mask.any():
                df_trakt.loc[mask, :] = pdf_converter.add_markdown_column(
                    df_trakt.loc[mask, :],
                    pdf_column,
                    method,
                    csv_output_path=csv_traktanden_md,
                )

    # Save updated DataFrame with markdown
    df_trakt.to_csv(csv_traktanden_md, index=False)

    columns_to_index = [
        "tag1",
        "text1",
        "tag2",
        "text2",
        "tag3",
        "text3",
        "gruppennummer",
        "gruppentitel",
        "status",
        "kommission",
        "departement",
    ]
    create_sqlite_table(
        db_path,
        df_trakt,
        "Tagesordnungen und Traktandenlisten",
        columns_to_index=columns_to_index,
    )


def create_sqlite_table(db_path, df, table_name, columns_to_index=None):
    """
    Create a SQLite dataset from a DataFrame.

    Args:
        db_path (str): The path to the SQLite database file.
        df (pd.DataFrame): The DataFrame containing the data.
        table_name: Name of the table to create in the database.
        columns_to_index (list): List of columns to create indices on.
    """
    if columns_to_index is None:
        columns_to_index = []
    logging.info(f"Creating SQLite database at {db_path}...")
    conn = sqlite3.connect(db_path)

    # Write the DataFrame to the SQLite database
    df.to_sql(name=table_name, con=conn, if_exists="replace", index=False)

    # Create indices for faster querying
    common.create_indices(conn, table_name, columns_to_index)

    conn.close()
    logging.info(f"SQLite database created successfully at {db_path}!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info(f"Executing {__file__}...")
    main()
    logging.info("Job successful")
s
