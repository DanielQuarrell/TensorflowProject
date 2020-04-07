using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using SimpleJSON;
public class JsonLoader : MonoBehaviour
{
    [SerializeField] string MapJsonPath;
    [SerializeField] int distanceMultiplier;

    [Header("Tile Prefabs")]
    [SerializeField] GameObject city_building;
    [SerializeField] GameObject dense_trees;
    [SerializeField] GameObject grass;
    [SerializeField] GameObject road;
    [SerializeField] GameObject sand;
    [SerializeField] GameObject sparse_trees;
    [SerializeField] GameObject village_building;
    [SerializeField] GameObject water;

    int width;
    int height;
    JSONArray tiles;
    TileMapScript tileMap;

    private void Awake()
    {
        tileMap = GetComponent<TileMapScript>();
    }

    void Start()
    {
        LoadJsonData();
        CreateMap();
    }

    void LoadJsonData()
    {
        string jsonString = File.ReadAllText(MapJsonPath);
        JSONNode json = JSON.Parse(jsonString);

        width = json["width"].AsInt;
        height = json["height"].AsInt;

        tiles = json["map_data"].AsArray;
    }

    void CreateMap()
    {
        for (int h = 0; h < height; h++)
        {
            for (int w = 0; w < width; w++)
            {
                switch (tiles[w + h * width].Value)
                {
                    case "city_building":
                        GameObject cityTile = Instantiate(city_building, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(cityTile, TileMapScript.TileTypes.city_building, new Vector2(w, h));
                        break;
                    case "dense_trees":
                        GameObject d_treeTile = Instantiate(dense_trees, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(d_treeTile, TileMapScript.TileTypes.dense_trees, new Vector2(w, h));
                        break;
                    case "grass":
                        GameObject grassTile = Instantiate(grass, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(grassTile, TileMapScript.TileTypes.grass, new Vector2(w, h));
                        break;
                    case "road":
                        GameObject roadTile = Instantiate(road, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(roadTile, TileMapScript.TileTypes.road, new Vector2(w, h));
                        break;
                    case "sand":
                        GameObject sandTile = Instantiate(sand, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(sandTile, TileMapScript.TileTypes.sand, new Vector2(w, h));
                        break;
                    case "sparse_trees":
                        GameObject s_treeTile = Instantiate(sparse_trees, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(s_treeTile, TileMapScript.TileTypes.sparse_trees, new Vector2(w, h));
                        break;
                    case "village_building":
                        GameObject villageTile = Instantiate(village_building, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(villageTile, TileMapScript.TileTypes.village_building, new Vector2(w, h));
                        break;
                    case "water":
                        GameObject waterTile = Instantiate(water, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        tileMap.AddTile(waterTile, TileMapScript.TileTypes.water, new Vector2(w, h));
                        break;
                }
            }
        }

        tileMap.RefreshAllTiles();
    }
}
