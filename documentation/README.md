# README

This program has two main files

 - heatmap.py
 - zoo.py

Inside heatmap.py you will find the UI used for retrieving user input needed for generating a heatmap. The class HeatMapOptionsBox is a top level tkinter object and in the constructor we setup all the fields, as well as a dictionary to store all the input, which will be modified when the user clicks the submit button. To retrieve the input from this class, supply it with a dictionary, and a key to place the options inside of that dictionary, like so: 

```python
plot_options = {'heatmap_options': {}}
heat_options_box = HeatMapOptionsBox(data_frame, (plot_options, 'heatmap_options'))
```

the first argument is the data_frame, which is how the UI knows the columns of the spreadsheet to display in the OptionMenus, and the second argument is the (dictionary,key) tuple.

Inside zoo.py you will find the rest of the program, which includes the code for the start page, and the graph page. The important code though, is in the constructor of the HeatMapPage class, this is where the data from the user input, as well as the spreadsheet, is combined in order to create a specialized graph. Inside the constructor the important things that happen are: 

* ```python
  cal_ratio = self.get_calibration_ratio(data_frame, options)
  ```

  * if the user included calibration point indices in their input, we get a ratio later used to translate the x and y points to be the same unit as the z points. (this returns 1 if the user did not input all the required values)

* ```python
  if options['begin_index'] != '' and options['end_index'] != '':
      data_frame = data_frame.iloc[int(options['begin_index']):int(options['end_index'])]
  ```

  * here we are shrinking the dataset to only include the values on the rows between the two given indices

* ```python
  for k, v in options['filters'].items():
      data_frame = data_frame.loc[(data_frame[k] == v)]
  ```
  * here we are looping over all custom column filters input by the user, and filtering the data_frame for each one. 

* ```python
  q_low = data_frame[self.x_col].quantile(0.01)
  q_hi = data_frame[self.x_col].quantile(0.99)
  
  data_frame = data_frame[(data_frame[self.x_col] < q_hi) &
                          (data_frame[self.x_col] > q_low)]
  ```

  * here we are removing statistical outliers from the set of points

* ```python
  if options['name_column'] != '':
      names = data_frame[options['name_column']].unique()
      self.filter_names_from_user_options(names, options)
      colors = cm.rainbow(np.linspace(0, 1, len(names)))
      for i in range(len(names)):
          name = names[i]
          color = colors[i]
          df_filtered = data_frame.loc[data_frame[options['name_column']] == name]
          self.x = df_filtered[self.x_col].values.flatten()
          self.y = df_filtered[self.y_col].values.flatten()
          self.x /= cal_ratio
          self.y /= cal_ratio
          if self.z_col != '':
              self.z = df_filtered[self.z_col].values.flatten()
              self.z *= -1
              hull = ss.ConvexHull(np.vstack((self.x,self.y,self.z)).T)
              self.ax.scatter(self.x, self.y, self.z, color=color, label=name+": "+str(hull.volume) + " " + options['unit_type'] + "$^{3}$")
          else:
              self.ax.scatter(self.x, self.y, color=color, label=name, picker=True)
      self.ax.legend()
  ```

  * in this block of code we are handling the branch where we want to plot the points with a different color based on the name column input by the user.
  * when the filter_names_From_user_options function is called, it checks if the user input any names in the comma seperated list, and if so, removes all other names from the names list, thus causing the code above to only plot the points with the names included by the user.
  * there is also code in here for calculating the total volume used by each set of points, on the line where hull is declared, and on the following line the call to hull.volume.

* ```python
  else:
      self.x = data_frame[self.x_col].values.flatten()
      self.y = data_frame[self.y_col].values.flatten()
      self.x /= cal_ratio
      self.y /= cal_ratio
      if self.z_col != '':
          self.z = data_frame[self.z_col].values.flatten()
          self.z *= -1
          self.ax = fig.add_subplot(111, projection='3d')
          self.ax.scatter(self.x, self.y, self.z, color='#1f77b4')
      else:
          self.ax = fig.add_subplot(111)
          self.ax.scatter(self.x, self.y, color='#1f77b4', picker=True)
  ```

  * and this is the other branch of code where we just generate the plot with all points as the same color