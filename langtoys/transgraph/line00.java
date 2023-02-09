import javafx.application.Application;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.shape.ArcType;
import javafx.stage.Stage;

public class line00 extends Application {
  
  public static void main(String[] args) {
    launch(args);
  }

  @Override
  public void start(Stage primaryStage) {
    primaryStage.setTitle("ToyLanguages");
    Group root = new Group();
    Canvas canvas = new Canvas(900, 600);
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
    for(int i=0;i<180;i++){
      gc.strokeLine(100,250+200*Math.sin(t*0.1),800,250+200*Math.cos(t*0.1));
      t+=3;
    }
  }
  
}
