using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileMapScript : MonoBehaviour
{
    public enum TileTypes
    {
        empty,
        city_building,
        dense_trees,
        grass,
        road,
        sand,
        sparse_trees,
        village_building,
        water,
    }

    List<TileScript> tiles = new List<TileScript>();

    public static TileMapScript instance;

    private void Awake()
    {
        instance = this;
    }

    public void AddTile(GameObject _tile, TileTypes _type, Vector2 _position)
    {
        TileScript tileScript = _tile.GetComponent<TileScript>();
        tileScript.type = _type;
        tileScript.position = _position;

        tiles.Add(tileScript);
    }

    public void RefreshAllTiles()
    {
        foreach (TileScript tile in tiles)
        {
            tile.RefreshTile();
        }
    }

    public bool IsSameType(TileTypes _type, Vector2 _position)
    {
        foreach(TileScript tile in tiles)
        {
            if(tile.position == _position)
            {
                if (tile.type == _type)
                {
                    return true;
                }
            }
        }

        return false;
    }

    public void RefreshTileAtPosition(Vector2 _position)
    {
        foreach (TileScript tile in tiles)
        {
            if (tile.position == _position)
            {
                tile.RefreshTile();
            }
        }
    }
}
