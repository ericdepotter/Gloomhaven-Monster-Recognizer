// Fill out your copyright notice in the Description page of Project Settings.


#include "BoundingBoxHUD.h"
#include "Math/Box2D.h"
#include "Math/Color.h"

void ABoundingBoxHUD::DrawHUD() 
{
    Super::DrawHUD();

    for (FBox2D BoundingBox: BoundingBoxesToDraw)
    {
        FLinearColor Color = FLinearColor::MakeRandomColor();
        
        DrawRect
        (
            Color.CopyWithNewOpacity(0.4),
            BoundingBox.Min.X,
            BoundingBox.Min.Y,
            BoundingBox.Max.X - BoundingBox.Min.X,
            BoundingBox.Max.Y - BoundingBox.Min.Y
        );
    }

}

bool ABoundingBoxHUD::AddBoundingBox(FBox2D BoundingBox) 
{
    BoundingBoxesToDraw.Add(BoundingBox);
    return true;
}
