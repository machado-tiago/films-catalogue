package service;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import model.Avaliacao;
import model.Movie;
import model.Usuario;
import repository.MovieRepository;
import repository.UsuarioRepository;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@ApplicationScoped
public class AvaliacaoService {

    @Inject
    MovieService movieService;

    @Inject
    UsuarioRepository usuarioRepository;

    public Avaliacao avaliar(Long idFilme, int nota, Long idUsuario) {
        Avaliacao avaliacao = new Avaliacao();
        return movieService.buscarPorId(idFilme)
                .map(
                movie -> {
                    return usuarioRepository.findByIdOptional(idUsuario)
                        .map(
                        usuario -> {
                            avaliacao.setUsuario(usuario);
                            avaliacao.setMovie(movie);
                            avaliacao.setDataAvaliacao(LocalDateTime.now());
                            avaliacao.setNota(nota);

                            return avaliacao;
                            })
                        .orElseThrow(()-> new RuntimeException("Usuário não encontrado"));
                })
                .orElseThrow(()-> new RuntimeException("Filme não encontrado"));

    }

    public BigDecimal calcularMediaAvaliacoes(Long idFilme) {

        return BigDecimal.ZERO;
    }
}
