package service;

import io.netty.util.AsyncMapping;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import model.Movie;
import repository.MovieRepository;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;

@ApplicationScoped
public class MovieService {

    @Inject
    MovieRepository movieRepository;

    @Inject
    EntityManager entityManager;

    public List<Movie> buscarTodos() {
        return movieRepository.listAll();
    }

    public Optional<Movie> buscarPorId(Long id) {
        return movieRepository.findByIdOptional(id);
    }

    public Movie criarRegistro(Movie movie) {
         movieRepository.persist(movie);
         return movie;
    }

    public Movie atualizar(Long id,  Movie movie) {
            movie.setId(id);    // garante que o ID está correto
            return  entityManager.merge(movie);     // merge() retorna a entidade "gerenciada" (sincronizada com o banco)
    }

    public boolean deletar(Long id) {
        return movieRepository.findByIdOptional(id)
                .map(movie ->{
                    movieRepository.delete(movie);
                    return true;
                } )
                .orElse(false);
    }
}
