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
                        Instantiate(city_building, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "dense_trees":
                        Instantiate(dense_trees, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "grass":
                        Instantiate(grass, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "road":
                        Instantiate(road, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "sand":
                        Instantiate(sand, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "sparse_trees":
                        Instantiate(sparse_trees, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "village_building":
                        Instantiate(village_building, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                    case "water":
                        Instantiate(water, new Vector3(w * distanceMultiplier, 0, h * distanceMultiplier), Quaternion.identity);
                        break;
                }
            }
        }
    }
}
