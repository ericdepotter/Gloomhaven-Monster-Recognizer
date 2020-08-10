// Fill out your copyright notice in the Description page of Project Settings.

#include "MyGameModeBase.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/GameplayStatics.h"
#include "Math/Box.h"
#include "Math/Box2D.h"
#include "Math/OrientedBox.h"
#include "Monster.h"

// Sets default values
AMonster::AMonster()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = _CMP_FALSE_OS;

	USceneComponent* Root = CreateDefaultSubobject<USceneComponent>(FName("RootSceneComponent"));
	Root->AttachToComponent(
		nullptr,
		FAttachmentTransformRules::SnapToTargetNotIncludingScale
	);

	SetRootComponent(Root);

	Standee = CreateDefaultSubobject<UStaticMeshComponent>(FName("Standee"));
	Standee->AttachToComponent(
		Root,
		FAttachmentTransformRules::SnapToTargetIncludingScale
	);

	Monster = CreateDefaultSubobject<UStaticMeshComponent>(FName("Monster"));
	Monster->AttachToComponent(
		Standee,
		FAttachmentTransformRules::SnapToTargetIncludingScale,
		TEXT("Monster")
	);
}

// Called when the game starts or when spawned
void AMonster::BeginPlay()
{
	Super::BeginPlay();
	
	GameMode = Cast<AMyGameModeBase>(UGameplayStatics::GetGameMode(GetWorld()));
	if (!GameMode)
	{
		UE_LOG(LogTemp, Error, TEXT("%s could not load game mode"), *GetName());
		return;
	}

	PlayerController = UGameplayStatics::GetPlayerController(GetWorld(), 0);
	if (!PlayerController)
	{
		UE_LOG(LogTemp, Error, TEXT("%s could not load player controller"), *GetName());
		return;
	}

	
	MonsterName = GameMode->GetRandomMonsterName();
	SwitchToTexture();
}

FBox2D AMonster::GetScreenBoundingBox() const
{
	//https://answers.unrealengine.com/questions/885132/how-to-create-tight-2d-bounding-boxes-for-actors-i.html
	//FBox BoundingBox = Monster->GetStaticMesh()->GetBoundingBox();
	FBox BoundingBox = GetComponentsBoundingBox(true);
	FVector Extent = BoundingBox.GetExtent();

	FOrientedBox oBox;
	oBox.Center = BoundingBox.GetCenter();
	oBox.ExtentX = Extent.X;
	oBox.ExtentY = Extent.Y;
	oBox.ExtentZ = Extent.Z;
	oBox.AxisX = GetActorRightVector();
	oBox.AxisY = GetActorForwardVector();
	oBox.AxisZ = GetActorUpVector();
	
	FVector OutVertices[8];
	oBox.CalcVertices(OutVertices);
	
	// Build 2D bounding box of actor in screen space
	FBox2D ActorBox2D(0);
	for (uint8 BoundsPointItr = 0; BoundsPointItr < 8; BoundsPointItr++)
	{
		FVector2D ScreenLocation;
		
		// Project vert into screen space.
		PlayerController->ProjectWorldLocationToScreen(OutVertices[BoundsPointItr], ScreenLocation, false);
		// Add to 2D bounding box
		ActorBox2D += ScreenLocation;// FVector2D(ProjectedWorldLocation.X, ProjectedWorldLocation.Y);
	}
	
	return ActorBox2D;
}

FString AMonster::GetMonsterName() const
{
	return MonsterName;
}