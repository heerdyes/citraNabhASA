/**
language: azakyAmUrtayantra
description: machine which executes an improbable instruction flow
interprets azakya files
*/

import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.shape.ArcType;
import javafx.stage.Stage;

class anuvAdaka{
  ArrayList<String> anekavAkya;
  String saJcikAsyanAma;
  
  anuvAdaka(String fn){
    anekavAkya=new ArrayList<String>();
    saJcikAsyanAma=fn;
  }
  
  void saMsAdhayati(){
    //
  }
}

public class azakyAmUrtayantrasaMsAdhaka extends Application {
  
  public static void main(String[] args) {
    launch(args);
  }

  @Override
  public void start(Stage primaryStage) {
    primaryStage.setTitle("azakyAmUrtayantra");
    Group root = new Group();
    Canvas canvas = new Canvas(#[width], #[height]);
    GraphicsContext gc = canvas.getGraphicsContext2D();
    try{
      genart(gc);
    }catch(Exception e){
      e.printStackTrace();
    }
    root.getChildren().add(canvas);
    primaryStage.setScene(new Scene(root));
    primaryStage.show();
  }

  private void genart(GraphicsContext gc) throws Exception {
    //
  }
  
}

