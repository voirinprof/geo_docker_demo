"""
Démo Docker pour la géomatique.

Ce script charge un jeu de secteurs (polygones simplifiés, à but
pédagogique), reprojette les données dans le système de coordonnées
cible du cours (EPSG:32198), puis calcule la superficie de chaque
secteur en kilomètres carrés.

Le but n'est pas l'analyse en elle-même, mais de montrer qu'un
environnement Docker fournit tout ce qu'il faut (Python + GDAL +
GeoPandas) sans rien installer sur la machine hôte.
"""

import geopandas as gpd

DATA_PATH = "data/secteurs.geojson"
TARGET_CRS = "EPSG:32198"  # MTM Québec, CRS cible du cours


def load_sectors(path):
    """Charge les secteurs depuis un fichier GeoJSON."""
    print(f"[1/3] Lecture de {path}...")
    gdf = gpd.read_file(path)
    print(f"      {len(gdf)} secteurs chargés (CRS d'origine : {gdf.crs})")
    return gdf


def reproject(gdf, target_crs):
    """Reprojette le GeoDataFrame vers le CRS cible."""
    print(f"[2/3] Reprojection vers {target_crs}...")
    return gdf.to_crs(target_crs)


def compute_areas(gdf):
    """Calcule la superficie de chaque secteur en km²."""
    print("[3/3] Calcul des superficies...")
    gdf = gdf.copy()
    gdf["superficie_km2"] = gdf.geometry.area / 1_000_000
    return gdf


def main():
    gdf = load_sectors(DATA_PATH)
    gdf = reproject(gdf, TARGET_CRS)
    gdf = compute_areas(gdf)

    print("\nRésultats :")
    for _, row in gdf.iterrows():
        print(f"  - {row['nom']:<15} {row['superficie_km2']:.2f} km²")


if __name__ == "__main__":
    main()
