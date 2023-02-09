import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.shape.ArcType;
import javafx.stage.Stage;

public class zero extends Application {
  
  public static void main(String[] args) {
    launch(args);
  }

  @Override
  public void start(Stage primaryStage) {
    primaryStage.setTitle("ToyLanguages");
    Group root = new Group();
    Canvas canvas = new Canvas(800, 600);
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
    var t=0;
    for(int i=0;i<50;i++){
      gc.strokeLine(200,50+t,300,50+t);
      t+=4;
    }
  }
  
}
