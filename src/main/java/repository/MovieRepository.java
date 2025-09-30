package repository;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import model.Movie;

@ApplicationScoped
public class MovieRepository implements PanacheRepository<Movie> {
}
