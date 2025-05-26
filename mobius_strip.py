import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm


class MobiusStrip:
    """
    A class representing a Mobius strip in 3D space.
    
    Attributes:
        R (float): Radius of the strip (distance from center)
        w (float): Width of the strip
        n (int): Resolution (number of points in the mesh)
        u_vals (ndarray): Array of u parameter values
        v_vals (ndarray): Array of v parameter values
        mesh (tuple): Tuple containing X, Y, Z coordinate arrays of points on the surface
    """
    
    def __init__(self, R=3.0, w=1.0, n=100):
        """
        Initialize the Mobius strip with given parameters.
        
        Args:
            R (float): Radius of the strip
            w (float): Width of the strip
            n (int): Resolution (number of points in the mesh)
        """
        self.R = R
        self.w = w
        self.n = n
        
        # Create parameter grids
        self.u_vals = np.linspace(0, 2*np.pi, n)
        self.v_vals = np.linspace(-w/2, w/2, n)
        
        # Generate the mesh
        self.mesh = self._generate_mesh()
    
    def _generate_mesh(self):
        """
        Generate the 3D mesh of points on the Mobius strip.
        
        Returns:
            tuple: X, Y, Z coordinate arrays of the mesh
        """
        # Create meshgrid for parameters
        u, v = np.meshgrid(self.u_vals, self.v_vals)
        
        # Calculate x, y, z coordinates using parametric equations
        x = (self.R + v * np.cos(u/2)) * np.cos(u)
        y = (self.R + v * np.cos(u/2)) * np.sin(u)
        z = v * np.sin(u/2)
        
        return x, y, z
    
    def calculate_surface_area(self):
        """
        Calculate the surface area of the Mobius strip numerically.
        
        Returns:
            float: Approximate surface area
        """
        # For surface area, we need to calculate the Jacobian determinant
        # and integrate ||∂r/∂u × ∂r/∂v|| over the parameter domain
        
        # Step size for parameters
        du = 2*np.pi / (self.n - 1)
        dv = self.w / (self.n - 1)
        
        # Initialize surface area
        surface_area = 0.0
        
        # Loop through parameter space (excluding edges to avoid boundary issues)
        for i in range(1, self.n-1):
            u = self.u_vals[i]
            
            for j in range(1, self.n-1):
                v = self.v_vals[j]
                
                # Partial derivatives with respect to u
                dx_du = -v/2 * np.sin(u/2) * np.cos(u) - (self.R + v * np.cos(u/2)) * np.sin(u)
                dy_du = -v/2 * np.sin(u/2) * np.sin(u) + (self.R + v * np.cos(u/2)) * np.cos(u)
                dz_du = v/2 * np.cos(u/2)
                
                # Partial derivatives with respect to v
                dx_dv = np.cos(u/2) * np.cos(u)
                dy_dv = np.cos(u/2) * np.sin(u)
                dz_dv = np.sin(u/2)
                
                # Cross product of partial derivatives
                cross_x = dy_du * dz_dv - dz_du * dy_dv
                cross_y = dz_du * dx_dv - dx_du * dz_dv
                cross_z = dx_du * dy_dv - dy_du * dx_dv
                
                # Magnitude of cross product
                magnitude = np.sqrt(cross_x**2 + cross_y**2 + cross_z**2)
                
                # Add contribution to surface area
                surface_area += magnitude * du * dv
        
        return surface_area
    
    def calculate_edge_length(self):
        """
        Calculate the length of the edge of the Mobius strip.
        
        Returns:
            float: Approximate edge length
        """
        # The edge corresponds to v = w/2 or v = -w/2
        # We'll calculate length for v = w/2
        
        edge_length = 0.0
        v = self.w/2
        
        # Previous point
        prev_x = (self.R + v * np.cos(0)) * np.cos(0)
        prev_y = (self.R + v * np.cos(0)) * np.sin(0)
        prev_z = v * np.sin(0)
        
        # Loop through u values to calculate edge length
        for i in range(1, self.n):
            u = self.u_vals[i]
            
            # Current point
            curr_x = (self.R + v * np.cos(u/2)) * np.cos(u)
            curr_y = (self.R + v * np.cos(u/2)) * np.sin(u)
            curr_z = v * np.sin(u/2)
            
            # Calculate distance to previous point
            dist = np.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2 + (curr_z - prev_z)**2)
            edge_length += dist
            
            # Update previous point
            prev_x, prev_y, prev_z = curr_x, curr_y, curr_z
        
        return edge_length
    
    def visualize(self, show_wireframe=True, show_surface=True, cmap='viridis'):
        """
        Visualize the Mobius strip.
        
        Args:
            show_wireframe (bool): Whether to show the wireframe
            show_surface (bool): Whether to show the surface
            cmap (str): Colormap for the surface
            
        Returns:
            tuple: Figure and axis objects
        """
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        X, Y, Z = self.mesh
        
        if show_wireframe:
            ax.plot_wireframe(X, Y, Z, color='k', alpha=0.2, linewidth=0.5)
        
        if show_surface:
            surf = ax.plot_surface(X, Y, Z, cmap=cmap, alpha=0.8, edgecolor='none')
            fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        
        # Plot the edge (v = w/2) - more robust approach
        edge_idx = np.abs(self.v_vals - self.w/2).argmin()
        ax.plot(X[edge_idx, :], Y[edge_idx, :], Z[edge_idx, :], 'r-', linewidth=2, label='Edge')
        
        # Plot the center line (v = 0) - more robust approach
        center_idx = np.abs(self.v_vals - 0).argmin()
        ax.plot(X[center_idx, :], Y[center_idx, :], Z[center_idx, :], 'b-', linewidth=2, label='Center line')
        
        ax.set_title(f'Mobius Strip (R={self.R}, w={self.w})')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        
        # Set aspect ratio to be equal
        max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0
        mid_x = (X.max()+X.min()) / 2.0
        mid_y = (Y.max()+Y.min()) / 2.0
        mid_z = (Z.max()+Z.min()) / 2.0
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        plt.tight_layout()
        return fig, ax


# Example usage
if __name__ == "__main__":
    # Create a Mobius strip
    mobius = MobiusStrip(R=3.0, w=1.0, n=100)
    
    # Calculate and print geometric properties
    surface_area = mobius.calculate_surface_area()
    edge_length = mobius.calculate_edge_length()
    
    print(f"Surface Area (approx): {surface_area:.4f}")
    print(f"Edge Length (approx): {edge_length:.4f}")
    
    # Visualize the strip
    fig, ax = mobius.visualize(show_wireframe=True, show_surface=True, cmap='viridis')
    plt.show()