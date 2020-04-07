using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileScript : MonoBehaviour
{
    [HideInInspector] public Vector2 position;
    [HideInInspector] public TileMapScript.TileTypes type;

    [SerializeField] private Sprite[] tileSprites;
    [SerializeField] private Sprite preview;

    [SerializeField] string ID;

    Renderer renderer;

    private void Awake()
    {
        renderer = this.GetComponent<Renderer>();
    }

    public void RefreshTile()
    {
        switch (type)
        {
            case TileMapScript.TileTypes.road:
            case TileMapScript.TileTypes.water:
                GetTileData();
                break;
            case TileMapScript.TileTypes.grass:
            case TileMapScript.TileTypes.sand:
                GetGrassSandData();
                break;
        }
    }

    public void GetTileData()
    {
        string directory = string.Empty;
        switch (type)
        {
            case TileMapScript.TileTypes.road:
                directory = "Textures/Road/";
                break;

            case TileMapScript.TileTypes.water:
                directory = "Textures/Water/";
                break;
        }

        if (directory != null)
        {
            string tileData = string.Empty;

            for (int y = -1; y <= 1; y++)
            {
                for (int x = 1; x >= -1; x--)
                {
                    if (!(x == 0 && y == 0))
                    {
                        if (Mathf.Abs(x) != Mathf.Abs(y))
                        {
                            Vector2 neighborPos = new Vector2(position.x + x, position.y + y);

                            if (TileMapScript.instance.IsSameType(type, neighborPos))
                            {
                                tileData += '1';
                            }
                            else
                            {
                                tileData += '0';
                            }
                        }
                    }
                }
            }

            ID = tileData;

            string texturePath = directory + tileData;
            Texture tex = Resources.Load(texturePath) as Texture;
            if (tex != null)
            {
                renderer.material.mainTexture = tex;
            }
            else
            {
                texturePath = directory + "0000";
                renderer.material.mainTexture = Resources.Load(texturePath) as Texture;
            }
        }
    }

    public void GetGrassSandData()
    {
        TileMapScript.TileTypes typeCheck = TileMapScript.TileTypes.empty;
        string directory = string.Empty;

        switch(type)
        {
            case TileMapScript.TileTypes.grass:
                typeCheck = TileMapScript.TileTypes.sand;
                directory = "Textures/Grass-Sand/";
                break;

            case TileMapScript.TileTypes.sand:
                typeCheck = TileMapScript.TileTypes.grass;
                directory = "Textures/Sand-Grass/";
                break;
        }

        string tileData = string.Empty;

        for (int y = -1; y <= 1; y++)
        {
            for (int x = 1; x >= -1; x--)
            {
                if (!(x == 0 && y == 0))
                {
                    if (Mathf.Abs(x) == Mathf.Abs(y))
                    {
                        Vector2 neighborPos = new Vector2(position.x + x, position.y + y);

                        if (TileMapScript.instance.IsSameType(typeCheck, neighborPos))
                        {
                            tileData += '1';
                        }
                        else
                        {
                            tileData += '0';
                        }
                    }
                }
            }
        }

        ID = tileData;

        string texturePath = directory + tileData;
        Texture tex = Resources.Load(texturePath) as Texture;
        if (tex != null)
        {
            renderer.material.mainTexture = tex;
        }
        else
        {
            renderer.material.mainTexture = Resources.Load(directory + "1111") as Texture;
        }
    }
}
